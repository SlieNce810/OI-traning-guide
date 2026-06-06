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


def normalize_section_heading(dir_name):
    """Convert directory name to section heading for SUMMARY.md consistency.

    "1.1-思维的体操" -> "1.1 思维的体操"
    "2.2-递 推 关 系" -> "2.2 递推关系"
    "3.8-动态树与LCT" -> "3.8 动态树与LCT"
    """
    # Split at the first hyphen after the numeric prefix (e.g., "1.1-")
    m = re.match(r'^(\d+\.\d+)-(.*)', dir_name)
    if m:
        prefix = m.group(1)
        rest = m.group(2)
        # Normalize spaces in the rest (e.g., "递 推 关 系" -> "递推关系")
        rest = re.sub(r'\s+', '', rest)
        return f'{prefix} {rest}'
    return dir_name


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
        # Make section heading match SUMMARY.md format:
        # Directory name "1.1-思维的体操" -> heading "1.1 思维的体操"
        heading_section = normalize_section_heading(section_name)
        lines.append(f"## {heading_section}\n")

        for cpp_file in cpp_files:
            cpp_path = os.path.join(section_path, cpp_file)
            title = extract_title(cpp_path)

            lines.append(f"### {title}\n")
            lines.append("```cpp")
            # Read and embed the source code directly (mdBook {{#include}} with
            # Unicode paths outside src/ is unreliable across CI environments)
            try:
                with open(cpp_path, 'r', encoding='utf-8') as f:
                    code = f.read().rstrip('\n')
                lines.append(code)
            except Exception:
                lines.append(f"// Source file: {section_name}/{cpp_file}")
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
