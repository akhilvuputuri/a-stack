#!/usr/bin/env python3
"""Offline, explicit-target installation. Never opens the runtime handoff store."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import shutil
import tempfile
import sys

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ("publish-handoff", "resume-handoff")
VERSION = "0.1.1"


def source_file(relative):
    """Only regular allowlisted source files; never follow symlinked ancestors."""
    candidate = ROOT
    for part in Path(relative).parts:
        if part in (".", "..") or Path(relative).is_absolute():
            raise ValueError("Invalid source path")
        candidate = candidate / part
        if candidate.is_symlink():
            raise ValueError("Source files and their parent directories must not be symlinks: " + relative)
    if not candidate.is_file():
        raise ValueError("Expected a regular source file: " + relative)
    return candidate


def recognized_installation(destination):
    # Inspect only expected code folders; refuse unknown entries without descending into them.
    expected = {
        destination: {"SKILL.md", "scripts", "references", ".a-stack-version"},
        destination / "scripts": {"relay.py", "handoff.schema.json"},
        destination / "references": {"handoff.md"},
    }
    for directory, names in expected.items():
        if directory.is_symlink() or not directory.is_dir() or set(os.listdir(directory)) != names:
            raise ValueError("Installation contains unexpected files or symlinks; preserve and inspect it before updating")
        for name in names:
            entry = directory / name
            if entry.is_symlink():
                raise ValueError("Installation contains symlinks; automatic replacement is not supported")
            if name not in ("scripts", "references") and not entry.is_file():
                raise ValueError("Expected code files must be regular files; preserve unexpected entries before updating")
    marker = destination / ".a-stack-version"
    if not marker.is_file() or marker.read_text().strip() not in ("0.1.0", VERSION):
        raise ValueError("Unknown installation/version; automatic replacement is not supported")


def install(target, names, replace=False):
    target = Path(target).expanduser().absolute()
    if target.is_symlink():
        raise ValueError("Installation target must not be a symlink")
    target = target.resolve()
    # No runtime-data traversal. Only compare lexical/canonical paths.
    data = Path(os.environ.get("ASTACK_DATA_DIR", "~/.local/share/a-stack")).expanduser().absolute()
    # Canonicalize only the trusted parent, without opening/traversing the store itself.
    data = data.parent.resolve() / data.name
    if target == data or target.is_relative_to(data) or data.is_relative_to(target):
        raise ValueError("Skill installation and runtime data directories must be separate")
    if target == ROOT or target.is_relative_to(ROOT / "skills"):
        raise ValueError("Do not overwrite source skills; use a separate installation target")
    target.mkdir(parents=True, exist_ok=True)
    installed = []
    for name in names:
        destination = target / name
        if destination.is_symlink():
            raise ValueError(f"Refusing symlink destination: {destination}")
        if destination.exists() and not replace:
            raise ValueError(f"{name} exists; use --replace for a code-only update")
        backup = target / ("." + name + ".previous")
        if backup.exists() or backup.is_symlink():
            raise ValueError(f"Previous installation backup exists: {backup}; inspect it before retrying")
        stage = Path(tempfile.mkdtemp(prefix="." + name + "-", dir=target))
        moved = False
        try:
            # Explicit allowlist: runtime records, fixtures, and diagnostics are never packaged.
            shutil.copyfile(source_file("skills/" + name + "/SKILL.md"), stage / "SKILL.md")
            (stage / "scripts").mkdir()
            shutil.copyfile(source_file("tools/relay.py"), stage / "scripts/relay.py")
            shutil.copyfile(source_file("schema/handoff.schema.json"), stage / "scripts/handoff.schema.json")
            (stage / "references").mkdir()
            shutil.copyfile(source_file("docs/handoff.md"), stage / "references/handoff.md")
            (stage / ".a-stack-version").write_text(VERSION + "\n")
            if destination.exists():
                # Only replace installations bearing our version marker, never arbitrary user folders.
                recognized_installation(destination)
                os.rename(destination, backup)
                moved = True
            os.rename(stage, destination)
            if moved:
                shutil.rmtree(backup)
            installed.append(str(destination))
        except BaseException:
            if moved and not destination.exists() and backup.exists():
                os.rename(backup, destination)
            raise
        finally:
            if stage.exists():
                shutil.rmtree(stage)
    return installed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    destination = parser.add_mutually_exclusive_group(required=True)
    destination.add_argument("--target", help="Custom agent skill-discovery directory")
    destination.add_argument("--agent", choices=("codex", "claude-code"), help="User-scoped installation for this agent")
    parser.add_argument("--version", action="version", version=VERSION)
    parser.add_argument("--skill", action="append", choices=SKILLS)
    parser.add_argument("--replace", action="store_true", help="Code-only update of a recognized installation")
    args = parser.parse_args()
    try:
        if sys.version_info < (3, 11) or os.name != "posix":
            raise ValueError("a-stack requires Python 3.11+ on macOS/Linux")
        target = args.target or Path.home() / (".agents/skills" if args.agent == "codex" else ".claude/skills")
        print(json.dumps({"version": VERSION, "installed": install(target, args.skill or SKILLS, args.replace)}, indent=2))
        return 0
    except (OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
