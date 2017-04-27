"""
Compare fonts from fonts.google.com which match fonts in a local 
repo of google/fonts.

Find families which are not in fonts.google.com.

Find families which are not in local repo of google/fonts
"""
import sys
import hashlib
import pandas as pd

from settings import production_fonts_dir
from hotfix2 import get_fonts

from fontTools.ttLib import TTFont

WIN_NAME_SUFFIXES = [
    " Thin",
    " ExtraLight",
    " Extralight",
    " SemiLight",
    " Light",
    " Regular",
    " Medium",
    " SemiBold",
    " Semibold",
    " Bold",
    " ExtraBold",
    " Extrabold",
    " Black",
    " VF Beta",

]

def get_familyname(ttfont):
    """Get the name of a font file"""
    name = ttfont['name'].getName(1, 3, 1, 1033).string
    name = name.decode('utf_16_be')
    for suffix in WIN_NAME_SUFFIXES:
        if suffix in name:
            name = name.replace(suffix, '')
    return name


def hash_files(files):
    hashes = {}
    for f in files:
        checksum = hash_file(f)
        hashes[checksum] = f
    return hashes


def hash_file(f):
    checksum = hashlib.md5(open(f, 'rb').read()).hexdigest()
    return checksum


def main(fonts_tree_path):
    
    repo_fonts = get_fonts(fonts_tree_path)
    prod_fonts = get_fonts(production_fonts_dir)
    
    repo_hashed_fonts = hash_files(repo_fonts)
    prod_hashed_fonts = hash_files(prod_fonts)

    l_hashes = set(repo_hashed_fonts.keys())
    r_hashes = set(prod_hashed_fonts.keys())
    
    compatible_fonts_hashes = l_hashes & r_hashes
    repo_compatible_fonts = [repo_hashed_fonts[h] for h in compatible_fonts_hashes]
    repo_incompatible_fonts = [f for f in repo_fonts
                               if f not in repo_compatible_fonts]

    repo_font_families_names = set([get_familyname(TTFont(f)) for f in repo_fonts])
    prod_font_families_names = set([get_familyname(TTFont(f)) for f in prod_fonts])
    
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
        'fonts.google.com missing'
    ]
    df.to_csv('./reports/repo_vs_production.csv', sep='\t', encoding='utf-8', index=False)

if __name__ == '__main__':
    main(sys.argv[-1])
