"""
Run font checks.

Checks are conducted on fonts which match betweeen fonts.google.com
and a local version google/fonts repo.
"""
import sys
from fontTools.ttLib import TTFont
import pandas as pd

import fontdata
import checks


def main(root_path):
    repo_vs_production = pd.read_csv('./reports/repo_vs_production.csv', sep='\t')
    compatible_fonts = repo_vs_production['google/fonts compatible files']

    table = []
    for font_path in compatible_fonts:
        font = TTFont(font_path)

        table.append([
            font_path,

            font['OS/2'].fsSelection,
            get_fsselection(font),
            checks.check_fsselection(font),

            font['head'].macStyle,
            get_macstyle(font),
            checks.check_macstyle(font),

            checks.check_name_table(font, font_path),

            font['OS/2'].fsType,
            0,
            check_fstype(font)
        ])

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
    # return overview CSV
    df = pd.DataFrame(table, columns=columns)
    df.to_csv('./reports/hotfix_overview.csv', sep='\t', encoding='utf-8', index=False)

    # passed families only
    df_passed = df[(df.macstyle == 'PASS') & (df.fsselection == 'PASS') & (df.fstype == 'PASS') & (df.nametable == 'PASS')]
    df_passed.to_csv('./reports/hotfix_passed.csv', sep='\t', encoding='utf-8', index=False)

    # failed families only
    df_failed = df[(df.macstyle == 'FAIL') | (df.fsselection == 'FAIL') | (df.fstype == 'FAIL') | (df.nametable == 'FAIL')]
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
