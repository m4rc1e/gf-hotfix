"""
Run font checks.

Generates reports which are written to ./reports
"""
from fontTools.ttLib import TTFont
import pandas as pd

from fontbakery import fontdata
from fontbakery import gfspec
import blacklist
from fontbakery import utils


def check_font_attrib(real, desired):
    if str(real) == str(desired):
        return [real, desired, 'PASS']
    return [real, desired, 'FAIL']


def check_nametable(real_nametable, desired_nametable):
    check_names = []
    nameids = [1, 2, 4, 6, 16, 17]
    for nameid in nameids:
        nameid_check = check_fname_field(
            real_nametable, desired_nametable, (nameid, 3, 1, 1033)
        )
        check_names.append(nameid_check)
    return check_names


def check_fname_field(real_name_tbl, desired_name_tbl, name):
    real, desired = None, None

    real = real_name_tbl.getName(*name)
    real = unicode(real.string, 'utf_16_be') if real else None

    desired = desired_name_tbl.getName(*name)
    desired = unicode(desired.string) if desired else None

    return check_font_attrib(real, desired)


def check_fonts(fonts_tree, report_suffix):

    font_paths = utils.get_fonts(fonts_tree)
    table = []
    for font_path in font_paths:
        font = TTFont(font_path)
        font_name = fontdata.get_familyname(font)

        if font_name not in blacklist.fonts:
            if font_name not in blacklist.existing_pr:

                gf_nametable = gfspec.get_nametable(font_path)

                check_fsselection = check_font_attrib(
                    font['OS/2'].fsSelection,
                    gfspec.get_fsselection(font, font_path)
                )
                check_macstyle = check_font_attrib(
                    font['head'].macStyle,
                    gfspec.get_macstyle(font_path)
                )
                check_weightclass = check_font_attrib(
                    font['OS/2'].usWeightClass,
                    gfspec.get_weightclass(font_path)
                )
                check_fstype = check_font_attrib(
                    font['OS/2'].fsType,
                    gfspec.FSTYPE
                )
                check_names = check_nametable(font['name'], gf_nametable)


                row = check_fsselection + \
                      check_macstyle + \
                      check_weightclass + \
                      check_fstype
                for check in check_names:
                    row += check


                row.insert(0, font_path)
                table.append(row)

    df_columns = [
        'file',

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
        'pref family name',

        'pref style name-F',
        'pref style name-W',
        'pref style name',
    ]
    # return collection wide overview CSV
    df = pd.DataFrame(table, columns=df_columns)
    df = df.sort(['family name-F', 'style name-F'])
    df.to_csv('./reports/%s_overview.csv' % report_suffix, sep='\t', encoding='utf-8', index=False)

    # # passed families only
    df_passed = df[
        (df['macstyle'] == 'PASS') & \
        (df['fsselection'] == 'PASS') & \
        (df['fstype'] == 'PASS') & \
        (df['weightclass'] == 'PASS') & \
        (df['fstype'] == 'PASS') & \
        (df['family name'] == 'PASS') & \
        (df['style name'] == 'PASS') & \
        (df['full name'] == 'PASS') & \
        (df['ps name'] == 'PASS') & \
        (df['pref family name'] == 'PASS') & \
        (df['pref style name'] == 'PASS')
    ]
    df_passed.to_csv('./reports/%s_passed.csv' % report_suffix, sep='\t', encoding='utf-8', index=False)

    # # failed families only
    df_failed = df[
        (df['macstyle'] == 'FAIL') | \
        (df['fsselection'] == 'FAIL') | \
        (df['fstype'] == 'FAIL') | \
        (df['weightclass'] == 'FAIL') | \
        (df['fstype'] == 'FAIL') | \
        (df['family name'] == 'FAIL') | \
        (df['style name'] == 'FAIL') | \
        (df['full name'] == 'FAIL') | \
        (df['ps name'] == 'FAIL') | \
        (df['pref family name'] == 'FAIL') | \
        (df['pref style name'] == 'FAIL')
    ]
    df_failed.to_csv('./reports/%s_failed.csv' % report_suffix, sep='\t', encoding='utf-8', index=False)

    failed_files = df_failed['file']
    failed_families = [fontdata.get_familyname(TTFont(p)) for p in failed_files]
    failed_families = list(set(failed_families))
    failed_families = sorted(failed_families)

    df_failed_families = pd.DataFrame(failed_families, columns=['family'])
    df_failed_families.to_csv('./reports/%s_failed_families.csv' % report_suffix, sep='\t', encoding='utf-8', index=False)
