import os
import sys
from fontTools.ttLib import TTFont
import unittest
import pandas as pd


def get_fonts(root_path):
    fonts = []
    for path, r, files in os.walk(root_path):
        for f in files:
            if f.endswith('.ttf'):
                fonts.append(os.path.join(path, f))
    return fonts


class TestFont(unittest.TestCase):
    def setUp(self):
        self.font = TTFont(font)


    def test_fsselection(ttfont):
        return ttfont['OS/2'].fsSelection


    def test_macstyle(ttfont):
        return ttfont['head'].macStyle


    def test_name_table(ttfont):
        return ttfont['name']


    def test_fstype(ttfont):
        return ttfont['OS/2'].fsType



def check_fsselection(ttfont):
    return ttfont['OS/2'].fsSelection


def check_macstyle(ttfont):
    return ttfont['head'].macStyle


def check_name_table(ttfont):
    return ttfont['name']


def check_fstype(ttfont):
    return ttfont['OS/2'].fsType


def main(root_path):
    fonts_path = get_fonts(root_path)

    table = []
    for font_path in fonts_path:
        font = TTFont(font_path)
        table.append([
            font_path,
            check_fsselection(font),
            check_macstyle(font),
            check_name_table(font),
            check_fstype(font)
        ])

    df = pd.DataFrame(table, columns=['file', 'fsselection', 'macstyle', 'name', 'fstype'])
    df.to_csv('gf_hotfix.csv', sep='\t', encoding='utf-8')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[-1])
    else:
        'please add path'
