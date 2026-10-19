#!/usr/bin/env python3
# Modified for safe packaging in oh-my-pi-config; see ../NOTICE.txt.
"""
Skill Packager - Creates a distributable .skill file of a skill folder

Usage:
    python utils/package_skill.py <path/to/skill-folder> [output-directory]

Example:
    python utils/package_skill.py skills/public/my-skill
    python utils/package_skill.py skills/public/my-skill ./dist
"""

import fnmatch
import os
import stat
import sys
import zipfile
from pathlib import Path
from scripts.quick_validate import validate_skill


def _path_has_symlink(path: Path) -> bool:
    """Return whether an existing component of path is a symbolic link."""
    current = path.absolute()
    while True:
        if current.is_symlink():
            return True
        if current.parent == current:
            return False
        current = current.parent


def _collect_files(skill_path: Path) -> list[tuple[Path, Path]]:
    """Collect regular files while rejecting links and out-of-root paths."""
    files = []
    for current_root, dirnames, filenames in os.walk(skill_path, followlinks=False):
        current = Path(current_root)
        unsafe_dirs = [current / name for name in dirnames if (current / name).is_symlink()]
        if unsafe_dirs:
            raise ValueError(f"Symbolic links are not allowed: {unsafe_dirs[0]}")
        for name in filenames:
            file_path = current / name
            if file_path.is_symlink():
                raise ValueError(f"Symbolic links are not allowed: {file_path}")
            metadata = file_path.stat()
            if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
                raise ValueError(f"Only unlinked regular files are allowed: {file_path}")
            resolved = file_path.resolve(strict=True)
            try:
                resolved.relative_to(skill_path)
            except ValueError as exc:
                raise ValueError(f"Input escapes skill directory: {file_path}") from exc
            arcname = file_path.relative_to(skill_path.parent)
            if should_exclude(arcname):
                print(f"  Skipped: {arcname}")
                continue
            files.append((file_path, arcname))
    return files

# Patterns to exclude when packaging skills.
EXCLUDE_DIRS = {"__pycache__", "node_modules"}
EXCLUDE_GLOBS = {"*.pyc"}
EXCLUDE_FILES = {".DS_Store"}
# Directories excluded only at the skill root (not when nested deeper).
ROOT_EXCLUDE_DIRS = {"evals"}


def should_exclude(rel_path: Path) -> bool:
    """Check if a path should be excluded from packaging."""
    parts = rel_path.parts
    if any(part in EXCLUDE_DIRS for part in parts):
        return True
    # rel_path is relative to skill_path.parent, so parts[0] is the skill
    # folder name and parts[1] (if present) is the first subdir.
    if len(parts) > 1 and parts[1] in ROOT_EXCLUDE_DIRS:
        return True
    name = rel_path.name
    if name in EXCLUDE_FILES:
        return True
    return any(fnmatch.fnmatch(name, pat) for pat in EXCLUDE_GLOBS)


def package_skill(skill_path, output_dir=None):
    """Package a skill folder into a new .skill archive."""
    requested_skill_path = Path(skill_path).expanduser()
    if _path_has_symlink(requested_skill_path):
        print(f"❌ Error: Symbolic links are not allowed in input path: {requested_skill_path}")
        return None
    try:
        skill_path = requested_skill_path.resolve(strict=True)
    except OSError:
        print(f"❌ Error: Skill folder not found: {requested_skill_path}")
        return None

    if not skill_path.is_dir():
        print(f"❌ Error: Path is not a directory: {skill_path}")
        return None

    skill_md = skill_path / "SKILL.md"
    if not skill_md.is_file() or skill_md.is_symlink():
        print(f"❌ Error: SKILL.md not found as a regular file in {skill_path}")
        return None

    output_path = (
        (Path(output_dir).expanduser() if output_dir else Path.cwd()).absolute()
    )
    if _path_has_symlink(output_path):
        print(f"❌ Error: Symbolic links are not allowed in output path: {output_path}")
        return None
    output_resolved = output_path.resolve()
    if output_resolved == skill_path or skill_path in output_resolved.parents:
        print("❌ Error: Output directory must not be inside the skill directory")
        return None
    if output_path.exists() and not output_path.is_dir():
        print(f"❌ Error: Output path is not a directory: {output_path}")
        return None

    try:
        files = _collect_files(skill_path)
    except (OSError, ValueError) as exc:
        print(f"❌ Error: Unsafe skill input: {exc}")
        return None

    print("🔍 Validating skill...")
    valid, message = validate_skill(skill_path)
    if not valid:
        print(f"❌ Validation failed: {message}")
        print("   Please fix the validation errors before packaging.")
        return None
    print(f"✅ {message}\n")

    skill_filename = output_path / f"{skill_path.name}.skill"
    if os.path.lexists(skill_filename):
        print(f"❌ Error: Refusing to overwrite existing output: {skill_filename}")
        return None

    try:
        output_path.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(skill_filename, "x", zipfile.ZIP_DEFLATED) as zipf:
            for file_path, arcname in files:
                zipf.write(file_path, arcname)
                print(f"  Added: {arcname}")
        print(f"\n✅ Successfully packaged skill to: {skill_filename}")
        return skill_filename
    except (OSError, zipfile.BadZipFile, ValueError) as exc:
        print(f"❌ Error creating .skill file: {exc}")
        return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python utils/package_skill.py <path/to/skill-folder> [output-directory]")
        print("\nExample:")
        print("  python utils/package_skill.py skills/public/my-skill")
        print("  python utils/package_skill.py skills/public/my-skill ./dist")
        sys.exit(1)

    skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"📦 Packaging skill: {skill_path}")
    if output_dir:
        print(f"   Output directory: {output_dir}")
    print()

    result = package_skill(skill_path, output_dir)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
