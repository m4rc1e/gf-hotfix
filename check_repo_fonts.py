"""
Run font checks.

Checks are conducted on fonts which match betweeen fonts.google.com
and a local version google/fonts repo.
"""
import sys
from fontTools.ttLib import TTFont
import pandas as pd

import fontdata
import gfspec


def check_font_attrib(real, desired):
    if str(real) == str(desired):
        return [real, desired, 'PASS']
    return [real, desired, 'FAIL']


def main(root_path):
    repo_vs_production = pd.read_csv('./reports/repo_vs_production.csv', sep='\t')
    # We only want to check fonts which match between the two sources
    compatible_files = repo_vs_production['google/fonts compatible files']

    table = []
    for font_path in compatible_files:
        font = TTFont(font_path)
        try:
            gf_nametable = gfspec.get_nametable(font_path)
        except:
            gf_nametable = None

        check_fsselection = check_font_attrib(
            font['OS/2'].fsSelection,
            gfspec.get_fsselection(font)
        )
        check_macstyle = check_font_attrib(
            font['head'].macStyle,
            gfspec.get_macstyle(font)
        )
        check_weightclass = check_font_attrib(
            font['OS/2'].usWeightClass,
            gfspec.get_weightclass(font, font_path)
        )
        check_fstype = check_font_attrib(
            font['OS/2'].fsType,
            gfspec.FSTYPE
        )
        try:
            gf_familyname = gf_nametable.getName(1, 3, 1, 1033).string.decode('utf_16_be')
            gf_stylename = gf_nametable.getName(2, 3, 1, 1033).string.decode('utf_16_be')
            gf_fullname = gf_nametable.getName(4, 3, 1, 1033).string.decode('utf_16_be')
            gf_psname = gf_nametable.getName(6, 3, 1, 1033).string.decode('utf_16_be')
            gf_pref_familyname = gf_nametable.getName(16, 3, 1, 1033).string.decode('utf_16_be')
        except:
            gf_familyname = gf_stylename = gf_fullname = gf_ps_name = None
            gf_pref_familyname = None

        check_familyname = check_font_attrib(
            font['name'].getName(1, 3, 1, 1033).string.decode('utf_16_be'),
            gf_familyname
        )
        check_stylename = check_font_attrib(
            font['name'].getName(2, 3, 1, 1033).string.decode('utf_16_be'),
            gf_stylename
        )
        check_fullname = check_font_attrib(
            font['name'].getName(4, 3, 1, 1033).string.decode('utf_16_be'),
            gf_fullname
        )
        check_psname = check_font_attrib(
            font['name'].getName(6, 3, 1, 1033).string.decode('utf_16_be'),
            gf_psname
        )
        if gf_pref_familyname:
            try:
                font_pref_familyname = font['name'].getName(16, 3, 1, 1033).string.decode('utf_16_be')
            except AttributeError:  # Font does not have this field
                font_pref_familyname = None

        check_pref_familyname = check_font_attrib(
            font_pref_familyname,
            gf_pref_familyname
        )
        row = check_fsselection + \
              check_macstyle + \
              check_weightclass + \
              check_fstype + \
              check_familyname + \
              check_stylename + \
              check_fullname + \
              check_psname + \
              check_pref_familyname


        row.insert(0, font_path)
        row.insert(1, fontdata.is_canonical(font_path))
        table.append(row)

    df_columns = [
        'file',
        'canonical',

        'fsselection-F',
        'fsselection-W',
        'fsselection',

        'macstyle-F',
        'macstyle-W',
        'macstyle',

        'weightclass-F',
        'weightclass-W',
        'weightclass',

        # 'nametable',
        'fstype-F',
        'fstype-W',
        'fstype',

        'family name-F',
        'family name-W',
        'family name',

        'style name-F',
        'style name-W',
        'style name',

        'full name-F',
        'full name-W',
        'full name',

        'ps name-F',
        'ps name-W',
        'ps name',

        'pref family name-F',
        'pref family name-W',
        'pref family name'
    ]
    # return overview CSV
    df = pd.DataFrame(table, columns=df_columns)
    df.to_csv('./reports/hotfix_overview.csv', sep='\t', encoding='utf-8', index=False)

    # # passed families only
    df_passed = df[(df['macstyle'] == 'PASS')]# & (df.fsselection == 'PASS') & (df.fstype == 'PASS') & (df.weightclass == 'PASS') & (df.nametable == 'PASS')]
    df_passed.to_csv('./reports/hotfix_passed.csv', sep='\t', encoding='utf-8', index=False)

    # # failed families only
    # df_failed = df[(df.macstyle == 'FAIL') | (df.fsselection == 'FAIL') | (df.fstype == 'FAIL') | (df.nametable == 'FAIL')]
    # df_failed.to_csv('./reports/hotfix_failed.csv', sep='\t', encoding='utf-8', index=False)

    # failed_files = df_failed['file']
    # failed_families = [fontdata.get_familyname(TTFont(p)) for p in failed_files]
    # failed_families = list(set(failed_families))
    # sorted(failed_families)

    # df_failed_families = pd.DataFrame(failed_families, columns=['family'])
    # df_failed_families.to_csv('./reports/hotfix_failed_families.csv', sep='\t', encoding='utf-8', index=False)



if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[-1])
    else:
        'please add google/fonts repo path'
