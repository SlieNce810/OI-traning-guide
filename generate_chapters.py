#!/usr/bin/env python3
"""
Auto-generate mdBook chapter and section markdown files.
Each section gets its own .md page — this is the standard mdBook approach
for reliable content rendering and section navigation.
"""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'src')

CHAPTERS = [
    ("第1章-算法设计基础", "第1章 算法设计基础"),
    ("第2章-数学基础", "第2章 数学基础"),
    ("第3章-实用数据结构", "第3章 实用数据结构"),
    ("第4章-几何问题", "第4章 几何问题"),
    ("第5章-图论算法与模型", "第5章 图论算法与模型"),
    ("第6章-更多算法专题", "第6章 更多算法专题"),
]


def natural_key(name):
    m = re.match(r'^(\d+)\.(\d+)', name)
    if m:
        return (int(m.group(1)), int(m.group(2)))
    return (999, 999)


def normalize_section_heading(dir_name):
    """Extract clean section name from directory name.
    '1.1-思维的体操' -> '思维的体操'
    """
    m = re.match(r'^\d+\.\d+-(.*)', dir_name)
    if m:
        rest = re.sub(r'\s+', '', m.group(1))
        return rest
    return dir_name


def extract_title(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('//') and len(line) > 2:
                    content = line[2:].strip()
                    if content:
                        return content
                elif line and not line.startswith('//'):
                    return os.path.splitext(os.path.basename(filepath))[0]
    except Exception:
        pass
    return os.path.splitext(os.path.basename(filepath))[0]


def section_file_name(section_dir_name, chapter_id):
    """Generate filename for a section page.
    '1.1-思维的体操' -> 'chapter1-section-1.1.md'
    """
    m = re.match(r'^(\d+\.\d+)', section_dir_name)
    if m:
        return f'chapter{chapter_id}-section-{m.group(1)}.md'
    return f'chapter{chapter_id}-section-{section_dir_name}.md'


def generate_summary(sections_by_chapter):
    """Generate SUMMARY.md from collected sections."""
    lines = ['# 目录\n', '- [前言](README.md)']

    for i, (ch_dir, ch_title) in enumerate(CHAPTERS, 1):
        secs = sections_by_chapter.get(i, [])
        if not secs:
            continue
        ch_file = f'chapter{i}.md'
        lines.append(f'- [{ch_title}]({ch_file})')
        for sec_num, sec_heading, sec_file in secs:
            lines.append(f'  - [{sec_num} {sec_heading}]({sec_file})')

    lines.append('- [勘误](Errata.md)')

    with open(os.path.join(SRC, 'SUMMARY.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    print('Generated SUMMARY.md')


def generate_all():
    os.makedirs(SRC, exist_ok=True)
    sections_by_chapter = {}  # chapter_id -> [(sec_num, sec_heading, sec_file)]

    for ch_id, (ch_dir, ch_title) in enumerate(CHAPTERS, 1):
        chapter_path = os.path.join(ROOT, ch_dir)
        if not os.path.isdir(chapter_path):
            continue

        # Generate chapter index page (just intro, no section content)
        ch_index = [f'# {ch_title}\n']
        ch_file = os.path.join(SRC, f'chapter{ch_id}.md')
        with open(ch_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(ch_index))

        # Collect and sort sections
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

            sec_heading = normalize_section_heading(name)
            m = re.match(r'^(\d+\.\d+)', name)
            sec_num = m.group(1) if m else name
            sec_file = section_file_name(name, ch_id)
            sec_path = os.path.join(SRC, sec_file)
            sections.append((sec_num, sec_heading, name, sec_path, section_path, cpp_files))

        sections_by_chapter[ch_id] = [
            (s[0], s[1], os.path.basename(s[3])) for s in sections
        ]

        # Generate each section page
        for sec_num, sec_heading, orig_name, sec_path, section_path, cpp_files in sections:
            lines = [f'# {sec_num} {sec_heading}\n']

            for cpp_f in cpp_files:
                cpp_path = os.path.join(section_path, cpp_f)
                title = extract_title(cpp_path)
                lines.append(f'## {title}\n')
                lines.append('```cpp')
                try:
                    with open(cpp_path, 'r', encoding='utf-8') as f:
                        code = f.read().rstrip('\n')
                    lines.append(code)
                except Exception:
                    lines.append(f'// Source: {orig_name}/{cpp_f}')
                lines.append('```\n')

            with open(sec_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))

        print(f'Chapter {ch_id}: {ch_title} ({len(sections)} sections)')

    generate_summary(sections_by_chapter)


if __name__ == '__main__':
    generate_all()
