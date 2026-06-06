#!/usr/bin/env python3
"""
Auto-generate chapter markdown files for mdBook.
Scans chapter directories, reads .cpp file headers, and generates
chapter pages with embedded code.
"""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'src')
CHAPTERS_DIR = ROOT  # chapters are at root level

# Chapter order / names
CHAPTERS = [
    ("第1章-算法设计基础", "第1章 算法设计基础"),
    ("第2章-数学基础", "第2章 数学基础"),
    ("第3章-实用数据结构", "第3章 实用数据结构"),
    ("第4章-几何问题", "第4章 几何问题"),
    ("第5章-图论算法与模型", "第5章 图论算法与模型"),
    ("第6章-更多算法专题", "第6章 更多算法专题"),
]


def natural_key(name):
    """Sort sections by numeric prefix (e.g., 1.1, 3.10)."""
    m = re.match(r'^(\d+)\.(\d+)', name)
    if m:
        return (int(m.group(1)), int(m.group(2)))
    return (999, 999)


def extract_title(filepath):
    """Extract problem title from the first comment line of a .cpp file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Match: // 例题N  name (EN, OJ ID)
                # or:    //   name (EN, OJ ID)
                if line.startswith('//') and len(line) > 2:
                    content = line[2:].strip()
                    if content:
                        return content
                elif line and not line.startswith('//'):
                    return os.path.splitext(os.path.basename(filepath))[0]
    except Exception:
        pass
    return os.path.splitext(os.path.basename(filepath))[0]


def generate_chapter(chapter_dir, chapter_title, chapter_id):
    """Generate one chapter markdown file."""
    chapter_path = os.path.join(CHAPTERS_DIR, chapter_dir)
    if not os.path.isdir(chapter_path):
        return

    # Collect sections
    sections = []
    for name in sorted(os.listdir(chapter_path), key=natural_key):
        section_path = os.path.join(chapter_path, name)
        if not os.path.isdir(section_path):
            continue
        cpp_files = sorted(
            [f for f in os.listdir(section_path) if f.endswith('.cpp')]
        )
        if not cpp_files:
            continue

        sections.append((name, section_path, cpp_files))

    # Build markdown
    lines = []
    lines.append(f"# {chapter_title}\n")

    for section_name, section_path, cpp_files in sections:
        # Generate heading ID matching SUMMARY.md
        # Keep Chinese chars but lowercase for ID consistency
        section_display = section_name.lstrip('0123456789.-')
        lines.append(f"## {section_name}\n")

        for cpp_file in cpp_files:
            cpp_path = os.path.join(section_path, cpp_file)
            title = extract_title(cpp_path)
            # Relative path from src/ to the .cpp file
            rel_path = os.path.relpath(cpp_path, SRC)

            lines.append(f"### {title}\n")
            lines.append(f"```cpp")
            lines.append(f'{{{{#include {rel_path}}}}}')
            lines.append("```\n")

    # Write file
    output_path = os.path.join(SRC, f"chapter{chapter_id}.md")
    os.makedirs(SRC, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"Generated {output_path} ({len(sections)} sections)")


def main():
    os.makedirs(SRC, exist_ok=True)

    for i, (dir_name, title) in enumerate(CHAPTERS, 1):
        generate_chapter(dir_name, title, i)


if __name__ == '__main__':
    main()
