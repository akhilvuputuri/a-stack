#!/usr/bin/env python3
"""Build Git-free installation artifacts from generic source only."""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path
import tempfile
import zipfile
import install
import package

RUNNER = '''import pathlib, sys, tempfile, zipfile
with tempfile.TemporaryDirectory(prefix="a-stack-install-") as scratch:
    root = pathlib.Path(scratch)
    with zipfile.ZipFile(sys.argv[0]) as archive:
        for name in archive.namelist():
            if not name.startswith("payload/"):
                continue
            relative = pathlib.PurePosixPath(name[len("payload/"):])
            if relative.is_absolute() or ".." in relative.parts:
                raise ValueError("Invalid installer payload path")
            target = root.joinpath(*relative.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(name))
    sys.path.insert(0, str(root / "tools"))
    import install
    sys.exit(install.main())
'''


def build(output):
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    version = install.VERSION
    installer = output / "a-stack-install.pyz"
    # Explicit source list; no runtime directory reads or archive extraction during build.
    payload = ["tools/install.py", "tools/relay.py", "schema/handoff.schema.json", "docs/handoff.md",
               "skills/publish-handoff/SKILL.md", "skills/resume-handoff/SKILL.md"]
    with zipfile.ZipFile(installer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("__main__.py", RUNNER)
        for relative in payload:
            archive.writestr("payload/" + relative, install.source_file(relative).read_bytes())
    skills_zip = output / f"a-stack-skills-{version}.zip"
    with tempfile.TemporaryDirectory(prefix="a-stack-build-") as scratch:
        staged = Path(scratch) / "skills"
        install.install(staged, install.SKILLS)
        with zipfile.ZipFile(skills_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for skill in install.SKILLS:
                for relative in ("SKILL.md", "scripts/relay.py", "scripts/handoff.schema.json", "references/handoff.md", ".a-stack-version"):
                    archive.write(staged / skill / relative, "skills/" + skill + "/" + relative)
    source = package.package(output / f"a-stack-source-{version}.tar.gz")
    files = [installer, skills_zip, source]
    sums = output / "SHA256SUMS"
    sums.write_text("".join(hashlib.sha256(path.read_bytes()).hexdigest() + "  " + path.name + "\n" for path in files))
    return files + [sums]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True)
    for path in build(parser.parse_args().output_dir):
        print(path)
