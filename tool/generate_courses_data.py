#!/usr/bin/env python3
import json
import os
import re
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any


PROJECT_ROOT = Path(__file__).resolve().parent.parent
COURSES_ROOT = PROJECT_ROOT / "src" / "core_courses"
OUTPUT_PATH = PROJECT_ROOT / "courses-data.json"


IGNORED_FILES = {".DS_Store", "Thumbs.db"}
IGNORED_DIRS = {".git", "__MACOSX"}


def _is_hidden(path: Path) -> bool:
    return path.name.startswith(".")


def _natural_sort_key(text: str):
    parts = re.split(r"(\d+)", text)
    key = []
    for p in parts:
        if p.isdigit():
            key.append(int(p))
        else:
            key.append(p.lower())
    return key


def _first_root_html(course_dir: Path) -> Optional[Path]:
    html_files = [
        p
        for p in course_dir.iterdir()
        if p.is_file()
        and p.suffix.lower() == ".html"
        and p.name not in IGNORED_FILES
        and not _is_hidden(p)
    ]
    html_files.sort(key=lambda p: _natural_sort_key(p.name))
    return html_files[0] if html_files else None


def _path_to_posix_relative(path: Path) -> str:
    return path.resolve().relative_to(PROJECT_ROOT).as_posix()


def _file_entry(path: Path) -> dict:
    try:
        size = path.stat().st_size
    except OSError:
        size = 0
    return {"name": path.name, "path": _path_to_posix_relative(path), "size": size}


def _build_tree(root: Path, *, exclude_file: Optional[Path] = None) -> Dict[str, Any]:
    tree: dict = {"folders": {}, "files": []}

    try:
        entries = list(root.iterdir())
    except OSError:
        return tree

    # folders first, then files; stable natural sort inside each group
    folders = [p for p in entries if p.is_dir()]
    files = [p for p in entries if p.is_file()]
    folders.sort(key=lambda p: _natural_sort_key(p.name))
    files.sort(key=lambda p: _natural_sort_key(p.name))

    for d in folders:
        if d.name in IGNORED_DIRS or _is_hidden(d):
            continue
        sub = _build_tree(d, exclude_file=exclude_file)
        if sub.get("folders") or sub.get("files"):
            tree["folders"][d.name] = sub

    for f in files:
        if f.name in IGNORED_FILES or _is_hidden(f):
            continue
        if exclude_file is not None and f.resolve() == exclude_file.resolve():
            continue
        tree["files"].append(_file_entry(f))

    return tree


def _parse_folder_name(folder_name: str) -> Tuple[str, str]:
    raw = folder_name or ""
    s = raw.strip()

    # Common patterns:
    # - CS5222-Computer Networks
    # - CS5222_Computer_Networks
    # - CS5222 Computer Networks
    m = re.match(r"^([A-Za-z]{2,}\d{3,4})(?:[-_\s]+)(.+)$", s)
    if m:
        code = m.group(1).strip()
        name = m.group(2).strip()
    else:
        parts = s.split()
        if parts and re.match(r"^[A-Za-z]{2,}\d{3,4}$", parts[0]):
            code = parts[0]
            name = " ".join(parts[1:]).strip() or s
        else:
            code = s or raw
            name = s or raw

    name = name.replace("_", " ")
    name = re.sub(r"\s{2,}", " ", name).strip()
    if code and name.lower().startswith(code.lower()):
        name = name[len(code) :].lstrip(" -_")

    return code or (s or raw), name or (s or raw)


def _is_template_folder(name: str) -> bool:
    # Skip placeholder template folder by default
    return "课程代码" in name or "[" in name or "]" in name


def generate() -> Dict[str, Any]:
    courses: List[Dict[str, Any]] = []

    if not COURSES_ROOT.exists():
        raise SystemExit(f"Missing courses root: {COURSES_ROOT}")

    for course_dir in sorted(
        [p for p in COURSES_ROOT.iterdir() if p.is_dir() and not _is_hidden(p)],
        key=lambda p: _natural_sort_key(p.name),
    ):
        if course_dir.name in IGNORED_DIRS:
            continue
        if _is_template_folder(course_dir.name):
            continue

        intro_html = _first_root_html(course_dir)
        tree = _build_tree(course_dir, exclude_file=intro_html)

        code, name = _parse_folder_name(course_dir.name)
        courses.append(
            {
                "id": course_dir.name,
                "folder": course_dir.name,
                "code": code,
                "name": name,
                "intro_html": _path_to_posix_relative(intro_html)
                if intro_html is not None
                else "",
                "files": tree,
            }
        )

    return {"courses_count": len(courses), "courses": courses}


def main() -> None:
    data = generate()
    OUTPUT_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"✅ Wrote {OUTPUT_PATH} ({data['courses_count']} courses)")


if __name__ == "__main__":
    main()
