#!/usr/bin/env python3

import pathlib
import re
import sys
from collections import defaultdict

WEIGHT_STRIDE = 10


class Article:
    FRONT_MATTER_MARKER = '+++'  # TOML front matter is a firm requirement
    WEIGHT_RE = re.compile(r'^\s*weight\s*=\s*([\d]+)', re.I)

    def __init__(self, path):
        self.path = path
        self.text_lines = path.read_text().splitlines()
        self.weight = None
        self.weight_line_index = None

        self.read_weight()

    def __str__(self):
        return str(self.path)

    @property
    def has_weight(self):
        return self.weight is not None

    def read_weight(self):
        in_front_matter = False

        for i, line in enumerate(self.text_lines):
            if line == self.FRONT_MATTER_MARKER:
                in_front_matter = not in_front_matter
                continue

            if in_front_matter:
                match = self.WEIGHT_RE.match(line)
                if match:
                    self.weight = int(match.group(1))
                    self.weight_line_index = i
                    break

    def set_weight(self, weight):
        self.weight = weight
        self.text_lines[self.weight_line_index] = f'weight = {weight}'

    def rewrite(self):
        text = ''.join(f'{line}\n' for line in self.text_lines)
        self.path.write_text(text)


class ArticleGroup:
    def __init__(self):
        self.articles = []
        self.weight_table = defaultdict(list)

    def add(self, article):
        self.articles.append(article)

        if article.has_weight:
            self.weight_table[article.weight].append(article)

    def get_incompletes(self):
        for article in self.articles:
            if not article.has_weight:
                yield article

    def get_conflicts(self):
        for weight in sorted(self.weight_table):
            articles = self.weight_table[weight]
            if len(articles) > 1:
                yield (weight, articles)

    def get_usable(self):
        for weight in sorted(self.weight_table):
            articles = self.weight_table[weight]
            assert len(articles) == 1
            yield articles[0]


class SafetyStop(Exception):
    pass


def main():
    root = pathlib.Path(__file__).resolve().parents[1]
    group = ArticleGroup()

    for article in (root / 'src' / 'content').rglob('*'):
        if not article.is_dir():
            try:
                group.add(Article(article))
            except UnicodeDecodeError:
                print(f'Skipping probable binary file {article}')

    should_stop = False
    for article in group.get_incompletes():
        should_stop = True
        print(f'Missing weight in {article}.')
    if should_stop:
        raise SafetyStop

    should_stop = False
    for weight, articles in group.get_conflicts():
        should_stop = True
        print(f'Duplicate weight {weight} in:')
        for article in articles:
            print(f'  - {article}')
    if should_stop:
        raise SafetyStop

    print(f'Renumbering articles using weight stride {WEIGHT_STRIDE}.')

    new_weight = WEIGHT_STRIDE
    for article in group.get_usable():
        print(f'Applying weight {new_weight} to {article}...')
        article.set_weight(new_weight)
        article.rewrite()
        new_weight += WEIGHT_STRIDE

    print('The deed is done.')


if __name__ == '__main__':
    try:
        main()
    except SafetyStop:
        print('Cannot continue.')
        sys.exit(1)
