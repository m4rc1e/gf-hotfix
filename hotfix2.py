import os
import sys
from fontTools.ttLib import TTFont
import pandas as pd

from nototools import font_data
from names import nametable_from_filename
from utils import get_fonts
import fontdata
def parse_metadata(font):
        """Parse font name to infer weight and slope."""
        font_name = font_data.font_name(font)
        bold = 'Bold' in font_name.split()
        italic = 'Italic' in font_name.split()
        return bold, italic


def get_fsselection(ttfont):
    try:
        bold, italic = parse_metadata(ttfont)
        fs_type = ((bold << 5) | italic) or (1 << 6)
        if italic:
            fs_type |= 1
        # check use_typo_metrics is enabled
        if 0b10000000 & ttfont['OS/2'].fsSelection:
            fs_type |= 128
        return fs_type
    except:
        all
        return None


def check_fsselection(ttfont):
    
    print ''
    expected_fs_type = get_fsselection(ttfont)
    print font_data.font_name(ttfont), ttfont['OS/2'].fsSelection, expected_fs_type
    return 'FAIL' if expected_fs_type != ttfont['OS/2'].fsSelection else 'PASS'


def get_macstyle(ttfont):
    try:
        bold, italic = parse_metadata(ttfont)
        mac_style = (italic << 1) | bold
        return mac_style
    except:
        all
        return None


def check_macstyle(ttfont):
    """Check the macStyle bit"""
    expected_mac_style = get_macstyle(ttfont)
    print font_data.font_name(ttfont), ttfont['head'].macStyle, expected_mac_style
    return 'FAIL' if ttfont['head'].macStyle != expected_mac_style else 'PASS'


def check_name_table(ttfont, font_path):
    nameids_to_check = [1, 2, 4, 6, 16, 17]
    passed = []
    nametable = ttfont['name']
    try:
        expected_nametable = nametable_from_filename(font_path)
    except:
        all
        return 'FAIL C'
    for field in nametable.names:
        name_id = field.nameID 
        if name_id in nameids_to_check:
            selected_field = (name_id, field.platformID, field.platEncID, field.langID)
            current_field = nametable.getName(*selected_field)
            expected_field = expected_nametable.getName(*selected_field)
            enc = current_field.getEncoding()

            if not expected_field:
                return 'FAIL'
            if str(current_field.string).decode(enc) != str(expected_field.string).decode(enc):
                passed.append('Fail')

    if 'FAIL' in passed:
        return 'FAIL'
    return 'PASS'


def check_fstype(ttfont):
    """fs type should be installable 0"""
    expected_fs_type = 0
    return 'FAIL' if ttfont['OS/2'].fsType != expected_fs_type else 'PASS'


def main(root_path):
    fonts_path = get_fonts(root_path)

    table = []
    failed = []
    columns = [
        'file',
        'fsselection-F',
        'fsselection-W',
        'fsselection',
        'macstyle-F',
        'macstyle-W',
        'macstyle',
        'nametable',
        'fstype-F',
        'fstype-W',
        'fstype'
    ]
    for font_path in fonts_path:
        font = TTFont(font_path)
        try:
            table.append([
                font_path,

                font['OS/2'].fsSelection,
                get_fsselection(font),
                check_fsselection(font),

                font['head'].macStyle,
                get_macstyle(font),
                check_macstyle(font),

                check_name_table(font, font_path),

                font['OS/2'].fsType,
                0,
                check_fstype(font)

            ])
        except:
            all
            table.append([
                font_path,

                font['OS/2'].fsSelection,
                get_fsselection(font),
                'FAIL',

                font['head'].macStyle,
                get_macstyle(font),
                'FAIL',

                'FAIL',

                font['OS/2'].fsType,
                0,
                check_fstype(font)])
            failed.append(font_path)

    print len(failed), ' FAILED', failed[:5]

    # return overview CSV
    df = pd.DataFrame(table, columns=columns)
    df.to_csv('./reports/hotfix_overview.csv', sep='\t', encoding='utf-8', index=False)

    # passed families only
    df_passed = df[(df.macstyle == 'PASS') | (df.fsselection == 'PASS') | (df.fstype == 'PASS')]
    df_passed.to_csv('./reports/hotfix_passed.csv', sep='\t', encoding='utf-8', index=False)

    # failed families only
    df_failed = df[(df.macstyle == 'FAIL') | (df.fsselection == 'FAIL') | (df.fstype == 'FAIL')]
    df_failed.to_csv('./reports/hotfix_failed.csv', sep='\t', encoding='utf-8', index=False)

    failed_files = df_failed['file']
    failed_families = [fontdata.get_familyname(TTFont(p)) for p in failed_files]
    failed_families = list(set(failed_families))
    sorted(failed_families)

    df_failed_families = pd.DataFrame(failed_families, columns=['family'])
    df_failed_families.to_csv('./reports/hotfix_failed_families.csv', sep='\t', encoding='utf-8', index=False)



if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[-1])
    else:
        'please add path'
