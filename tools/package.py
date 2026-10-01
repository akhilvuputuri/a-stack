#!/usr/bin/env python3
"""Package generic source using an allowlist; no runtime store access."""
import argparse
from pathlib import Path
import tarfile
from install import source_file

ROOT = Path(__file__).resolve().parent.parent


def package(destination):
    destination = Path(destination).resolve()
    allowed = ["README.md", "AGENTS.md", "REVIEW.md", ".gitignore", "VERSION", "tools/relay.py", "tools/install.py", "tools/package.py", "tools/build_release.py",
               "schema/handoff.schema.json", "docs/handoff.md", "docs/validation.md",
               "docs/development.md", "docs/installation-research.md", ".github/workflows/ci.yml",
               "skills/publish-handoff/SKILL.md", "skills/resume-handoff/SKILL.md",
               "tests/test_relay.py", "tests/offline_guard/sitecustomize.py",
               "evals/handoff/conversation.md", "evals/handoff/cases.json"]
    with tarfile.open(destination, "w:gz") as archive:
        for relative in allowed:
            source = source_file(relative)
            archive.add(source, arcname="a-stack/" + relative, recursive=False)
        # Include development links without following them; every target is already in the archive.
        for skill in ("publish-handoff", "resume-handoff"):
            for relative in (f"skills/{skill}/scripts/relay.py", f"skills/{skill}/references/handoff.md"):
                source = ROOT / relative
                if not source.is_symlink() or not source.resolve().is_relative_to(ROOT):
                    raise ValueError("Expected an internal development link: " + relative)
                archive.add(source, arcname="a-stack/" + relative, recursive=False)
    return destination


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    print(package(parser.parse_args().output))
