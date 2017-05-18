"""
Compare fonts in production against the fonts in google/fonts repository

Find families which are not in fonts.google.com.

Find families which are not in local repo of google/fonts
"""
import sys
import pandas as pd
from fontTools.ttLib import TTFont

from settings import production_fonts_dir, repo_cp_path
from fontbakery import fontdata
from fontbakery.utils import get_fonts, hash_files


def main():
    
    repo_fonts = get_fonts(repo_cp_path)
    prod_fonts = get_fonts(production_fonts_dir)
    
    repo_hashed_fonts = hash_files(repo_fonts)
    prod_hashed_fonts = hash_files(prod_fonts)

    l_hashes = set(repo_hashed_fonts.keys())
    r_hashes = set(prod_hashed_fonts.keys())
    
    compatible_fonts_hashes = l_hashes & r_hashes
    repo_compatible_fonts = [repo_hashed_fonts[h] for h in compatible_fonts_hashes]
    repo_incompatible_fonts = [f for f in repo_fonts
                               if f not in repo_compatible_fonts]

    repo_font_families_names = set([fontdata.get_familyname(TTFont(f)) for f in repo_fonts])
    prod_font_families_names = set([fontdata.get_familyname(TTFont(f)) for f in prod_fonts])
    
    repo_missing_families = prod_font_families_names - repo_font_families_names
    prod_missing_families = repo_font_families_names - prod_font_families_names

    repo_missing_families = list(repo_missing_families)
    prod_missing_families = list(prod_missing_families)

    sorted(repo_missing_families)
    sorted(prod_missing_families)    
    

    df = pd.concat(
        [
            pd.Series(repo_compatible_fonts),
            pd.Series(repo_incompatible_fonts),
            pd.Series(repo_missing_families),
            pd.Series(prod_missing_families),
        ],
        axis=1
    )
    df.columns = [
        'google/fonts compatible files',
        'google/fonts incompatible files',
        'google/fonts missing',
        'fonts.google.com missing',
    ]
    df.to_csv('./reports/repo_vs_production.csv', sep='\t', encoding='utf-8', index=False)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main()
    else:
        print 'include path to local version of google/fonts repo'
