import os
from fontTools.ttLib import TTFont
import pandas as pd
from ntpath import basename

import gfspec
import fontdata
from utils import get_fonts, delete_files


def fix_fonts(fonts_paths, families_to_fix, dest):
    for font_path in fonts_paths:
        fix_font(font_path, families_to_fix, dest)


def fix_font(font_path, families_to_fix, dest):
    """Fix fonts attribs to match GF Spec"""
    font = TTFont(font_path)
    font_name = fontdata.get_familyname(font)
    font_filename = basename(font_path)
    dest_path = os.path.join(dest, font_filename)

    if font_name in families_to_fix:
        nametable = gfspec.get_nametable(font_path)
        font['OS/2'].fsSelection = gfspec.get_fsselection(font, font_path)
        font['head'].macStyle = gfspec.get_macstyle(font_path)
        font['OS/2'].usWeightClass = gfspec.get_weightclass(font_path)
        font['OS/2'].fsType = gfspec.FSTYPE
        font['name'] = nametable
        font.save(dest_path)
    else:
        print 'Skipping %s, blacklisted' % font_name 
        print 'Font %s fixed and saved to %s' % (font_name, dest_path)


def main():
    broken_families_doc = pd.read_csv('./reports/hotfix_failed_families.csv', delimiter='\t', encoding='utf-8')
    broken_families = list(broken_families_doc['family'])

    renamed_prod_fonts = get_fonts('./bin/production_fonts_renamed')
    delete_files('./bin/production_fonts_fixed')
    fix_fonts(renamed_prod_fonts, broken_families, './bin/production_fonts_fixed')

if __name__ == '__main__':
    main()
