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
    marker = destination / ".a-stack-version"
    if not marker.is_file() or marker.read_text().strip() != "0.1.0":
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
            shutil.copyfile(ROOT / "skills" / name / "SKILL.md", stage / "SKILL.md")
            (stage / "scripts").mkdir()
            shutil.copyfile(ROOT / "tools/relay.py", stage / "scripts/relay.py")
            shutil.copyfile(ROOT / "schema/handoff.schema.json", stage / "scripts/handoff.schema.json")
            (stage / "references").mkdir()
            shutil.copyfile(ROOT / "docs/handoff.md", stage / "references/handoff.md")
            (stage / ".a-stack-version").write_text("0.1.0\n")
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
    parser.add_argument("--target", required=True, help="Agent's skill-discovery directory")
    parser.add_argument("--skill", action="append", choices=SKILLS)
    parser.add_argument("--replace", action="store_true", help="Replace only a recognized 0.1.0 code installation")
    args = parser.parse_args()
    try:
        print(json.dumps({"installed": install(args.target, args.skill or SKILLS, args.replace)}, indent=2))
        return 0
    except (OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
