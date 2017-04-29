import names
from nototools import font_data


STYLES = [
    "Thin",
    "ExtraLight",
    "Extralight",
    "SemiLight",
    "Light",
    "Regular",
    "Medium",
    "SemiBold",
    "Semibold",
    "Bold",
    "ExtraBold",
    "Extrabold",
    "Black",
    "VF Beta",
]

WEIGHTS = {
    "Thin": 250,
    "ExtraLight": 275,
    "Extralight": 275,
    "SemiLight": 275,
    "Light": 300,
    "Regular": 400,
    "Italic": 400,
    "Medium": 500,
    "SemiBold": 600,
    "Semibold": 600,
    "Bold": 700,
    "ExtraBold": 800,
    "Extrabold": 800,
    "Black": 900,
    "VF Beta": 400,
}

FSTYPE = 0


def get_macstyle(ttfont):
    bold, italic = parse_metadata(ttfont)
    mac_style = (italic << 1) | bold
    return mac_style


def get_fsselection(ttfont):
    bold, italic = parse_metadata(ttfont)
    fs_type = ((bold << 5) | italic) or (1 << 6)
    if italic:
        fs_type |= 1
    # check use_typo_metrics is enabled
    if 0b10000000 & ttfont['OS/2'].fsSelection:
        fs_type |= 128
    return fs_type


def get_weightclass_by_fullname(ttfont):
    """Return the desired OS/2 weightclass"""
    full_name = ttfont['name'].getName(4, 3, 1, 1033).string.decode('utf_16_be')
    for word in full_name.split():
        if word in WEIGHTS:
            return WEIGHTS[word]
    return None


def get_weightclass_by_stylename(ttfont):
    style_name = ttfont['name'].getName(2, 3, 1, 1033).string.decode('utf_16_be')
    for word in style_name.split():
        if word in WEIGHTS:
            return WEIGHTS[word]
    return None


def get_weightclass_by_filename(filename):
    for weight in WEIGHTS:
        if weight in filename:
            return WEIGHTS[weight]


def get_weightclass_by_name_tbl(ttfont):
    fullname = get_weightclass_by_fullname(ttfont)
    stylename = get_weightclass_by_stylename(ttfont)
    return fullname if fullname else stylename


def get_weightclass(ttfont, filename):
    """Infer the OS/2 usweightClass from the following sequence:

    Check the filename's suffix
    Check if nametable's fullname contains the style
    Check if the nametable's style name contains the style
    """
    weight_from_file = get_weightclass_by_filename(filename)
    weight_from_font = get_weightclass_by_name_tbl(ttfont)
    return weight_from_file if weight_from_file else weight_from_font


def parse_metadata(font):
        """Parse font name to infer weight and slope."""
        font_name = font_data.font_name(font)
        bold = 'Bold' in font_name.split()
        italic = 'Italic' in font_name.split()
        return bold, italic


def get_nametable(filepath, family_name=None, style_name=None):
    return names.nametable_from_filename(filepath, family_name=family_name, style_name=style_name)


if __name__ == '__main__':
    import pandas as pd 
    from fontTools.ttLib import TTFont
    repo_vs_production = pd.read_csv('./reports/repo_vs_production.csv', sep='\t')
    # We only want to check fonts which match between the two sources
    compatible_fonts = repo_vs_production['google/fonts compatible files']
    for file in compatible_fonts:
        font = TTFont(file)
        print file, get_weightclass(font, file)
