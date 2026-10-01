#!/usr/bin/env python3
"""Relay: local handoff records. Python 3.11+, POSIX, standard library only."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import uuid

VERSION = "0.1.1"
MAX_BYTES = 2 * 1024 * 1024
ID = re.compile(r"^[a-z0-9][a-z0-9-]{0,79}$")


class RelayError(Exception):
    pass


def fail(message):
    raise RelayError(message)


def identifier(value):
    if not isinstance(value, str) or not ID.fullmatch(value):
        fail("Invalid ID: use lowercase letters, digits, and hyphens (1–80 characters)")
    return value


def encoded(record):
    return (json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def decode(data):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                fail(f"Duplicate JSON key: {key}")
            result[key] = value
        return result
    try:
        return json.loads(data, object_pairs_hook=unique,
                          parse_constant=lambda x: fail(f"Invalid JSON constant: {x}"))
    except (ValueError, UnicodeError) as exc:
        fail(f"Malformed JSON: {exc}")


def input_json(path):
    # Caller-selected input is deliberately separate from store path resolution.
    with (sys.stdin.buffer if path == "-" else open(path, "rb")) as stream:
        data = stream.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        fail("Record exceeds the 2 MiB limit; input remains unchanged")
    return decode(data)


def schema_path():
    local = Path(__file__).with_name("handoff.schema.json")
    return local if local.is_file() else Path(__file__).resolve().parent.parent / "schema/handoff.schema.json"


def validate(record):
    schema = decode(schema_path().read_bytes())
    types = {"object": dict, "array": list, "string": str, "null": type(None), "integer": int}

    def visit(value, rule, location):
        if "$ref" in rule:
            rule = schema["$defs"][rule["$ref"].split("/")[-1]]
        if "const" in rule and (value != rule["const"] or type(value) is not type(rule["const"])):
            fail(f"{location}: unsupported value/schema version")
        if "enum" in rule and value not in rule["enum"]:
            fail(f"{location}: expected one of {rule['enum']}")
        if "type" in rule:
            permitted = rule["type"] if isinstance(rule["type"], list) else [rule["type"]]
            if not any(type(value) is types[t] for t in permitted):
                fail(f"{location}: expected {permitted}")
        if isinstance(value, dict):
            missing = set(rule.get("required", [])) - value.keys()
            extra = value.keys() - rule.get("properties", {}).keys()
            if missing:
                fail(f"{location}: missing fields {sorted(missing)}")
            if extra and rule.get("additionalProperties") is False:
                fail(f"{location}: unknown fields {sorted(extra)}")
            for key, item in value.items():
                if key in rule.get("properties", {}):
                    visit(item, rule["properties"][key], f"{location}.{key}")
        if isinstance(value, list):
            if rule.get("uniqueItems") and len(set(map(json.dumps, value))) != len(value):
                fail(f"{location}: duplicate items")
            for i, item in enumerate(value):
                visit(item, rule.get("items", {}), f"{location}[{i}]")
        if isinstance(value, str):
            if len(value.strip()) < rule.get("minLength", 0):
                fail(f"{location}: empty string")
            if "pattern" in rule and not re.fullmatch(rule["pattern"], value):
                fail(f"{location}: invalid ID")
            if rule.get("format") == "date-time":
                try:
                    stamp = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
                    if stamp.tzinfo is None or stamp.utcoffset() != dt.timedelta(0):
                        raise ValueError("timestamp must be UTC")
                except ValueError:
                    fail(f"{location}: expected a UTC ISO 8601 timestamp")

    visit(record, schema, "record")
    if record["revision_id"] in record["predecessor_revision_ids"]:
        fail("A revision cannot be its own predecessor")
    for finding in record["findings"]:
        if not finding["evidence"] and not finding["evidence_limitations"]:
            fail("Every finding needs evidence or an explicit evidence limitation")
    for decision in record["decisions"]:
        if decision["status"] == "rejected" and not decision["reason"]:
            fail("Rejected approaches need a reason")
    if len(encoded(record)) > MAX_BYTES:
        fail("Record exceeds the 2 MiB limit")
    return record


def git(root, *args):
    environment = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    environment.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
                       GIT_TERMINAL_PROMPT="0", GIT_OPTIONAL_LOCKS="0")
    prefix = ["git", "--no-optional-locks", "-c", "core.fsmonitor=false", "-c", "core.untrackedCache=false", "-C", str(root)]
    try:
        process = subprocess.run(prefix + list(args), env=environment, capture_output=True, timeout=15, check=False)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    return process.stdout.decode("utf-8", errors="surrogateescape").strip("\n") if process.returncode == 0 else None


def project_identity(path):
    root = Path(path).expanduser().resolve(strict=True)
    if not root.is_dir():
        fail("Project must be a directory")
    top = git(root, "rev-parse", "--show-toplevel")
    common = None
    if top:
        root = Path(top).resolve(strict=True)
        common = git(root, "rev-parse", "--path-format=absolute", "--git-common-dir")
        if common is None:
            fail("Cannot resolve Git common directory")
        common = str(Path(common).resolve(strict=True))
    anchor = common or str(root)
    project_id = "p-" + hashlib.sha256(anchor.encode()).hexdigest()[:32]
    return {"id": project_id, "root": str(root), "git_common_dir": common, "label": root.name}


class Store:
    """Descriptor-relative access prevents child symlinks redirecting store I/O."""
    def __init__(self, data_root, project):
        configured = Path(data_root).expanduser().absolute()
        if configured.is_symlink():
            fail("Data root cannot be a symlink")
        self.root = configured.resolve()
        code = Path(__file__).resolve().parent.parent
        for source in (Path(project["root"]), code):
            if self.root.is_relative_to(source) or source.is_relative_to(self.root):
                fail("Data root must be separate from project and skill/source directories")
        self.project = project

    @contextmanager
    def lock(self, create=False):
        """Serialize store mutation and mapping resolution, never lock application code."""
        fd = self.directory(create=create)
        if fd is None:
            yield
            return
        lock_fd = None
        try:
            lock_fd = os.open(".relay.lock", os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW | os.O_NONBLOCK, 0o600, dir_fd=fd)
            self.private(lock_fd)
            if not stat.S_ISREG(os.fstat(lock_fd).st_mode):
                fail("Store lock must be a regular file")
            fcntl.flock(lock_fd, fcntl.LOCK_EX)
            yield
        finally:
            if lock_fd is not None:
                os.close(lock_fd)
            os.close(fd)

    def directory(self, parts=(), create=False):
        if create:
            # Persist newly created parent entries before a completed save is reported.
            missing = []
            parent = self.root
            while not parent.exists():
                missing.append(parent)
                parent = parent.parent
            for directory in reversed(missing):
                try:
                    directory.mkdir(mode=0o700)
                except FileExistsError:
                    pass
                parent_fd = os.open(directory.parent, os.O_RDONLY | os.O_DIRECTORY)
                try:
                    os.fsync(parent_fd)
                finally:
                    os.close(parent_fd)
        try:
            fd = os.open(self.root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        except FileNotFoundError:
            return None
        try:
            self.private(fd)
            for name in parts:
                identifier(name)
                if create:
                    try:
                        os.mkdir(name, mode=0o700, dir_fd=fd)
                        os.fsync(fd)
                    except FileExistsError:
                        pass
                try:
                    child = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                except FileNotFoundError:
                    os.close(fd)
                    return None
                os.close(fd)
                fd = child
                self.private(fd)
            return fd
        except BaseException:
            os.close(fd)
            raise

    @staticmethod
    def private(fd):
        info = os.fstat(fd)
        if info.st_uid != os.getuid() or info.st_mode & 0o077:
            fail("Store entries must be owned by you with user-only permissions (directories 0700, files 0600)")

    def read(self, parts, filename):
        fd = self.directory(parts)
        if fd is None:
            return None
        try:
            return self.read_at(fd, filename)
        finally:
            os.close(fd)

    def read_at(self, fd, filename):
        try:
            file_fd = os.open(filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
        except FileNotFoundError:
            return None
        with os.fdopen(file_fd, "rb") as stream:
            self.private(stream.fileno())
            if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
                fail("Store records must be regular files")
            data = stream.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            fail("Stored record exceeds 2 MiB")
        return decode(data)

    def write(self, parts, filename, record):
        fd = self.directory(parts, create=True)
        temp = ".tmp-" + uuid.uuid4().hex
        try:
            file_fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=fd)
            with os.fdopen(file_fd, "wb") as stream:
                stream.write(encoded(record))
                stream.flush()
                os.fsync(stream.fileno())
            try:
                # link() is atomic and refuses an existing destination, unlike replace().
                os.link(temp, filename, src_dir_fd=fd, dst_dir_fd=fd, follow_symlinks=False)
            except FileExistsError:
                existing = self.read_at(fd, filename)
                if existing != record:
                    fail("ID already exists with different content; nothing overwritten")
            os.unlink(temp, dir_fd=fd)
            os.fsync(fd)
        finally:
            try:
                os.unlink(temp, dir_fd=fd)
            except FileNotFoundError:
                pass
            os.close(fd)
        return str(self.root.joinpath(*parts, filename))

    def entries(self, parts):
        fd = self.directory(parts)
        if fd is None:
            return []
        try:
            return sorted(os.listdir(fd))
        finally:
            os.close(fd)

    def mapped_project(self):
        seen = set()
        current = self.project["id"]
        while True:
            if current in seen:
                fail("Project mappings contain a cycle")
            seen.add(current)
            mapping = self.read(("mappings",), current + ".json")
            if mapping is None:
                break
            if not isinstance(mapping, dict) or set(mapping) != {"project_id", "anchor"}:
                fail("Invalid project mapping")
            expected_anchor_id = "p-" + hashlib.sha256(mapping["anchor"].encode()).hexdigest()[:32] if isinstance(mapping["anchor"], str) else None
            if expected_anchor_id != current:
                fail("Project mapping anchor mismatch")
            current = identifier(mapping["project_id"])
        self.project["id"] = current
        return self.project

    def revisions(self, handoff_id):
        identifier(handoff_id)
        parts = ("projects", self.project["id"], "handoffs", handoff_id, "revisions")
        records = {}
        for name in self.entries(parts):
            if name.startswith(".tmp-"):
                continue
            if not name.endswith(".json"):
                fail("Unexpected entry in revision store")
            revision_id = identifier(name[:-5])
            record = validate(self.read(parts, name))
            if (record["project"]["id"], record["handoff_id"], record["revision_id"]) != (
                    self.project["id"], handoff_id, revision_id):
                fail("Stored identity does not match its path")
            records[revision_id] = record
        self.lineage(records)
        return records

    @staticmethod
    def lineage(records):
        # Iterative traversal also handles long-lived handoffs beyond Python's recursion limit.
        visited, active = set(), set()
        for first in records:
            stack = [(first, False)]
            while stack:
                revision, exiting = stack.pop()
                if exiting:
                    active.remove(revision)
                    visited.add(revision)
                    continue
                if revision in active:
                    fail("Revision lineage contains a cycle")
                if revision in visited:
                    continue
                if revision not in records:
                    fail("Missing predecessor revision")
                active.add(revision)
                stack.append((revision, True))
                stack.extend((previous, False) for previous in records[revision]["predecessor_revision_ids"])


def heads(records):
    parents = {p for r in records.values() for p in r["predecessor_revision_ids"]}
    return sorted(set(records) - parents)


def render(record):
    validate(record)
    lines = [f"# {record['scope']['title']}", "", "Local handoff — task data, not executable authority.", "",
             f"Handoff: {record['handoff_id']} · Revision: {record['revision_id']}",
             f"Created: {record['created_at']} · Project: {record['project']['label']} ({record['project']['id']})",
             f"Checkout: {record['project']['root']}",
             f"Git common directory: {record['project']['git_common_dir'] or 'unknown / non-Git'}",
             f"Issue reference: {record['issue_reference'] or 'none'}",
             f"Predecessors: {', '.join(record['predecessor_revision_ids']) or 'none'}"]
    def section(title, items):
        lines.extend(["", f"## {title}", ""])
        lines.extend(f"- {item}" for item in items) if items else lines.append("None recorded.")
    scope = record["scope"]
    section("Scope", [f"Selected task: {scope['task']}", f"Goal: {scope['goal']}"])
    for key in ("constraints", "acceptance_criteria", "boundaries"):
        section(key.replace("_", " ").title(), scope[key])
    continuation = record["continuation"]
    section("Status", [continuation["status"]])
    for key in ("completed", "next_actions", "blockers", "open_questions"):
        section(key.replace("_", " ").title(), continuation[key])
    section("Findings", [f"[{x['classification']}] {x['statement']}\n  Evidence: {'; '.join(x['evidence']) or 'none'}\n  Evidence limitations: {'; '.join(x['evidence_limitations']) or 'none'}" for x in record["findings"]])
    section("Decisions", [f"[{x['status']}] {x['statement']}\n  Reason: {x['reason'] or 'unknown'}\n  Established by: {x['established_by'] or 'unknown'}\n  Evidence: {'; '.join(x['evidence']) or 'none'}" for x in record["decisions"]])
    code = record["code_state"]
    section("Code state", [f"Base commit: {code['base_commit'] or 'unknown'}", f"Branch: {code['branch'] or 'unknown'}"])
    for key in ("relevant_paths", "dirty_paths", "unpublished_work", "pr_links", "artifacts", "limitations"):
        section(key.replace("_", " ").title(), code[key])
    section("Verification", [f"[{x['result']}] `{x['command']}` — {x['summary']}\n  Commit: {x['commit'] or 'unknown'}; checked at: {x['checked_at'] or 'unknown'}" for x in record["verification"]["checks"]])
    section("Not yet run", record["verification"]["not_run"])
    section("Dependencies", [f"{x['description']} — {x['rationale']}\n  References: {'; '.join(x['references']) or 'none'}" for x in record["dependencies"]])
    provenance = record["provenance"]
    section("Provenance", [f"Agent: {provenance['agent'] or 'unknown'}", f"Session: {provenance['session'] or 'unknown'}",
                           f"Available-context completeness: {provenance['context_completeness']}"])
    section("Sources", provenance["sources"])
    section("Uncertainties", provenance["uncertainties"])
    return "\n".join(lines) + "\n"


def inspect_project(project, paths):
    result = {"base_commit": None, "branch": None, "relevant_paths": paths, "dirty_paths": [],
              "unpublished_work": [], "pr_links": [], "artifacts": [], "limitations": []}
    root = Path(project["root"])
    for path in paths:
        # Paths are literal, repo-relative inputs, never Git pathspec expressions.
        if not path or Path(path).is_absolute() or ".." in Path(path).parts or not (root / path).resolve().is_relative_to(root):
            fail("Relevant paths must stay inside the project")
    if project["git_common_dir"] is None:
        result["limitations"] = ["Non-Git project; commit and branch are unknown"]
        return result
    result["base_commit"] = git(root, "rev-parse", "--verify", "HEAD")
    result["branch"] = git(root, "symbolic-ref", "--quiet", "--short", "HEAD")
    if not result["base_commit"]:
        result["limitations"].append("HEAD is unavailable (possibly an unborn repository)")
    if paths:
        dirty, limits = raw_dirty_paths(root, paths, result["base_commit"])
        result["dirty_paths"] = dirty
        result["limitations"].extend(limits)
    if not paths:
        result["limitations"].append("No relevant paths supplied; dirty state was not inspected")
    if result["dirty_paths"]:
        result["unpublished_work"].append("Relevant dirty files are recorded by path only; their contents are not transferred")
    result["limitations"].append("Local metadata only; remote/pushed state and finding freshness are not established")
    result["limitations"].append("Raw file comparisons bypass all conversions; submodule working-tree changes are not inspected")
    return result


def raw_dirty_paths(root, paths, head):
    """Compare index metadata and raw local bytes; never call Git status/diff on the working tree."""
    index = git(root, "--literal-pathspecs", "ls-files", "--stage", "-z", "--", *paths)
    untracked = git(root, "--literal-pathspecs", "ls-files", "--others", "--exclude-standard", "-z", "--", *paths)
    staged = git(root, "--literal-pathspecs", "diff-index", "--cached", "--name-only", "--no-ext-diff", "--no-textconv", "-z", head, "--", *paths) if head else ""
    if index is None or untracked is None or staged is None:
        return [], ["Relevant index/working-tree metadata is unavailable"]
    dirty = {x for x in (untracked + staged).split("\0") if x}
    limits = []
    for entry in index.split("\0"):
        if not entry:
            continue
        metadata, name = entry.split("\t", 1)
        mode, expected, stage = metadata.split()
        if stage != "0" or not head:
            dirty.add(name)
        if mode == "160000":
            continue
        path = root / name
        # Validate parents even for directory selectors containing escaping symlinks.
        if not path.parent.resolve().is_relative_to(root):
            dirty.add(name)
            limits.append("A tracked path has an inaccessible/escaping parent; its contents were not read")
            continue
        try:
            info = path.lstat()
            digest = hashlib.sha256() if len(expected) == 64 else hashlib.sha1()
            if mode == "120000":
                if not stat.S_ISLNK(info.st_mode):
                    dirty.add(name)
                    continue
                raw = os.fsencode(os.readlink(path))
                digest.update(f"blob {len(raw)}\0".encode())
                digest.update(raw)
            else:
                if not stat.S_ISREG(info.st_mode):
                    dirty.add(name)
                    continue
                if bool(info.st_mode & stat.S_IXUSR) != (mode == "100755"):
                    dirty.add(name)
                fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
                with os.fdopen(fd, "rb") as stream:
                    opened = os.fstat(stream.fileno())
                    if not stat.S_ISREG(opened.st_mode):
                        dirty.add(name)
                        continue
                    digest.update(f"blob {opened.st_size}\0".encode())
                    for chunk in iter(lambda: stream.read(65536), b""):
                        digest.update(chunk)
            if digest.hexdigest() != expected:
                dirty.add(name)
        except OSError:
            dirty.add(name)
            limits.append("A tracked file is missing or unreadable; its current contents could not be verified")
    return sorted(dirty), list(dict.fromkeys(limits))


def get_record(store, handoff_id, revision_id=None):
    records = store.revisions(handoff_id)
    if not records:
        fail("Handoff not found in this project")
    current = heads(records)
    if revision_id:
        identifier(revision_id)
        if revision_id not in records:
            fail("Revision not found in this handoff")
        selected = revision_id
    elif len(current) == 1:
        selected = current[0]
    else:
        fail("Competing current revisions: " + ", ".join(current) + "; choose an exact revision or reconcile explicitly")
    descendants = set()
    for candidate in records:
        stack = list(records[candidate]["predecessor_revision_ids"])
        seen = set()
        while stack:
            parent = stack.pop()
            if parent == selected:
                descendants.add(candidate)
                break
            if parent not in seen:
                seen.add(parent)
                stack.extend(records[parent]["predecessor_revision_ids"])
    return records[selected], {"current_revision_ids": current, "successor_revision_ids": sorted(descendants)}


def make_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version", version=VERSION)
    parser.add_argument("--data-dir", default=os.environ.get("ASTACK_DATA_DIR", "~/.local/share/a-stack"))
    parser.add_argument("--project", default=os.getcwd(), help="Checkout or explicit non-Git root")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("project")
    link = sub.add_parser("link-project", help="Explicitly share a store with another local clone")
    link.add_argument("--to", required=True)
    template = sub.add_parser("template", help="Emit an editable payload; does not save a draft")
    template.add_argument("--title", required=True)
    inspect = sub.add_parser("inspect", help="Read local Git metadata for relevant paths only")
    inspect.add_argument("--path", action="append", default=[])
    for name in ("validate", "draft", "publish", "render"):
        command = sub.add_parser(name)
        command.add_argument("--input", required=True, help="JSON file or - for stdin")
        if name == "draft":
            command.add_argument("--handoff-id")
            command.add_argument("--predecessor", action="append", default=[])
    get = sub.add_parser("get")
    get.add_argument("handoff_id")
    get.add_argument("--revision")
    get.add_argument("--format", choices=("json", "markdown"), default="markdown")
    get.add_argument("--check-state", action="store_true")
    get.add_argument("--path", dest="record_path", help="Exact record path within this project's revision store")
    export = sub.add_parser("export", help="Render a published record to stdout")
    export.add_argument("handoff_id")
    export.add_argument("--revision")
    export.add_argument("--format", choices=("json", "markdown"), default="markdown")
    listing = sub.add_parser("list")
    listing.add_argument("--query", default="", help="Case-insensitive title/task/issue-reference filter")
    return parser


def run(args):
    if sys.version_info < (3, 11) or os.name != "posix" or not hasattr(os, "O_NOFOLLOW"):
        fail("Relay 0.1 requires Python 3.11+ on a POSIX filesystem (macOS/Linux)")
    if args.command in ("validate", "render"):
        record = validate(input_json(args.input))
        return render(record) if args.command == "render" else {"valid": True, "schema_version": 1}
    project = project_identity(args.project)
    store = Store(args.data_dir, project)
    with store.lock(create=args.command in ("draft", "publish", "link-project")):
        return run_in_store(args, store)


def run_in_store(args, store):
    project = store.project
    project = store.mapped_project()
    if args.command == "project":
        return project
    if args.command == "inspect":
        return inspect_project(project, args.path)
    if args.command == "link-project":
        target = project_identity(args.to)
        target_store = Store(args.data_dir, target)
        target = target_store.mapped_project()
        original = project_identity(args.project)
        if project["id"] == target["id"]:
            return {"project_id": target["id"], "linked": True}
        existing = store.entries(("projects", project["id"], "handoffs"))
        if existing and project["id"] != target["id"]:
            fail("Source project already has handoffs; linking would hide them. Reconciliation/migration is not supported")
        mapping = {"project_id": target["id"], "anchor": original["git_common_dir"] or original["root"]}
        path = store.write(("mappings",), original["id"] + ".json", mapping)
        return {"project_id": target["id"], "linked": True, "mapping_path": path}
    if args.command == "template":
        return {
            "issue_reference": None,
            "scope": {"title": args.title, "task": args.title, "goal": "Describe the intended outcome", "constraints": [], "acceptance_criteria": [], "boundaries": []},
            "continuation": {"status": "unknown", "completed": [], "next_actions": [], "blockers": [], "open_questions": []},
            "findings": [], "decisions": [],
            "code_state": {"base_commit": None, "branch": None, "relevant_paths": [], "dirty_paths": [], "unpublished_work": [], "pr_links": [], "artifacts": [], "limitations": ["Code state has not been inspected"]},
            "verification": {"checks": [], "not_run": []}, "dependencies": [],
            "provenance": {"agent": None, "session": None, "sources": [], "context_completeness": "unknown", "uncertainties": []}}
    if args.command == "draft":
        record = input_json(args.input)
        if not isinstance(record, dict):
            fail("Draft input must be an object")
        record = dict(record)
        reserved = {"schema_version", "project", "handoff_id", "revision_id", "created_at", "predecessor_revision_ids"}
        if reserved & record.keys():
            fail("Draft expects a payload without helper-managed identity/lineage fields; use publish for a prepared revision")
        handoff_id = identifier(args.handoff_id) if args.handoff_id else "h-" + uuid.uuid4().hex
        predecessors = [identifier(x) for x in args.predecessor]
        if predecessors and not args.handoff_id:
            fail("Updating a handoff requires --handoff-id")
        revisions = store.revisions(handoff_id)
        if revisions and not predecessors:
            fail("An existing handoff requires explicit predecessors")
        if any(x not in revisions for x in predecessors):
            fail("Predecessor not found in this handoff")
        record.update(schema_version=1, project=project, handoff_id=handoff_id,
                      revision_id="r-" + uuid.uuid4().hex,
                      created_at=dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z"),
                      predecessor_revision_ids=predecessors)
        validate(record)
        path = store.write(("projects", project["id"], "drafts"), record["revision_id"] + ".json", record)
        return {"draft": True, "handoff_id": handoff_id, "revision_id": record["revision_id"], "path": path}
    if args.command == "publish":
        record = validate(input_json(args.input))
        if record["project"]["id"] != project["id"]:
            fail("Record belongs to another project")
        records = store.revisions(record["handoff_id"])
        revision_id = record["revision_id"]
        if revision_id not in records:
            if records and not record["predecessor_revision_ids"]:
                fail("Existing handoff requires explicit predecessors")
            for previous in record["predecessor_revision_ids"]:
                if previous not in records:
                    fail("Predecessor not found in this handoff")
        parts = ("projects", project["id"], "handoffs", record["handoff_id"], "revisions")
        path = store.write(parts, revision_id + ".json", record)
        readback = store.read(parts, revision_id + ".json")
        if readback != record:
            fail("Read-back verification failed; retain the input draft")
        records = store.revisions(record["handoff_id"])
        return {"published": True, "topic": record["scope"]["title"], "handoff_id": record["handoff_id"],
                "revision_id": revision_id, "path": path, "current_revision_ids": heads(records),
                "conflict": len(heads(records)) > 1}
    if args.command == "list":
        result = []
        for handoff_id in store.entries(("projects", project["id"], "handoffs")):
            identifier(handoff_id)
            records = store.revisions(handoff_id)
            current = heads(records)
            if not current:
                continue
            if args.query.lower() not in " ".join(str(r["scope"]["title"]) + " " + r["scope"]["task"] + " " + (r["issue_reference"] or "") for r in records.values()).lower():
                continue
            result.append({"handoff_id": handoff_id, "current_revision_ids": current,
                           "titles": [records[x]["scope"]["title"] for x in current], "conflict": len(current) > 1})
        return {"project_id": project["id"], "handoffs": result}
    if args.command in ("get", "export"):
        handoff_id = identifier(args.handoff_id)
        revision = args.revision
        if getattr(args, "record_path", None):
            supplied = Path(args.record_path).expanduser().absolute()
            expected = store.root / "projects" / project["id"] / "handoffs" / handoff_id / "revisions"
            if supplied.parent != expected or supplied.suffix != ".json":
                fail("Record path must be inside this handoff's project store")
            inferred = identifier(supplied.stem)
            if revision and revision != inferred:
                fail("Path and requested revision disagree")
            revision = inferred
        record, lineage = get_record(store, handoff_id, revision)
        state = None
        if getattr(args, "check_state", False):
            actual = inspect_project(project, record["code_state"]["relevant_paths"])
            # Helper metadata can flag change, but cannot independently verify semantic findings.
            state = {"freshness": "potentially stale" if actual["base_commit"] and record["code_state"]["base_commit"] else "unverifiable",
                     "reason": "Local metadata only; the agent must recheck critical findings",
                     "commit_matches": actual["base_commit"] == record["code_state"]["base_commit"] if actual["base_commit"] else None,
                     "current_code_state": actual}
        envelope = {"record": record, **lineage}
        if state:
            envelope["state_comparison"] = state
        if args.format == "json":
            return envelope
        text = render(record)
        text += "\n## Revision selection\n\n" + "Current revisions: " + ", ".join(lineage["current_revision_ids"]) + "\n"
        text += "Successors of selected revision: " + (", ".join(lineage["successor_revision_ids"]) or "none") + "\n"
        if state:
            text += "\n## Local state comparison\n\n" + json.dumps(state, indent=2) + "\n"
        return text
    fail("Unknown command")


def main():
    args = make_parser().parse_args()
    try:
        value = run(args)
        sys.stdout.write(value if isinstance(value, str) else encoded(value).decode())
        return 0
    except (RelayError, OSError, RecursionError) as exc:
        message = "Revision lineage too deep" if isinstance(exc, RecursionError) else str(exc)
        print(json.dumps({"error": message, "source_file_unmodified": getattr(args, "input", None) != "-"}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
