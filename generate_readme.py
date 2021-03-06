#!/usr/bin/env python

import os
import re
from dataclasses import dataclass
from operator import attrgetter
from typing import List, Optional


@dataclass
class Note:
    filepath: str
    category: str
    title: str
    created_at: str


def get_title(filepath: str) -> str:
    with open(filepath) as note:
        return next(note).strip('#').strip()


def get_date(file: str) -> Optional[str]:
    match = re.search(r'(\d{4}-\d{2}-\d{2})', file)
    if match:
        return match.group(0)

    return ''


def get_notes() -> List[Note]:
    results = []

    for root, dirs, files in os.walk("."):
        if root == '.':
            for dir_ in list(dirs):
                if dir_.startswith('.'):
                    dirs.remove(dir_)
            continue

        for file in files:
            if not file.endswith('.md'):
                continue

            basedir = os.path.basename(root)
            filepath = os.path.join(basedir, file)

            results.append(
                Note(
                    filepath=filepath,
                    created_at=get_date(file),
                    category=basedir,
                    title=get_title(filepath),
                )
            )

    return results


def sort_notes(notes: List[Note]) -> List[Note]:
    title_asc = sorted(notes, key=attrgetter('title'))
    created_at_desc = sorted(title_asc, key=attrgetter('created_at'), reverse=True)
    category_asc = sorted(created_at_desc, key=attrgetter('category'))
    return category_asc


def generate_header() -> str:
    with open('.notes/header.md', 'r') as content_file:
        return content_file.read()


def generate_category(category: str) -> str:
    return f'\n### {category}\n\n'


def generate_item(note: Note) -> str:
    if note.created_at:
        return f'- [{note.title.lower()}]({note.filepath}) - {note.created_at}\n'

    return f'- [{note.title.lower()}]({note.filepath})\n'


def generate_footer() -> str:
    with open('.notes/footer.md', 'r') as content_file:
        return content_file.read()


def generate_readme_content(notes: List[Note]):
    content = generate_header()

    category = None

    for note in notes:
        if note.category != category:
            category = note.category
            content += generate_category(category)

        content += generate_item(note)

    content += generate_footer()
    return content


def main():
    notes = sort_notes(get_notes())

    content = generate_readme_content(notes)
    with open('README.md', 'w') as readme:
        readme.write(content)


if __name__ == '__main__':
    main()
