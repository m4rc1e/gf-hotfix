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

def get_familyname(ttfont):
    """Get the name of a font file"""
    name = ttfont['name'].getName(1, 3, 1, 1033).string
    name = name.decode('utf_16_be')
    for style in STYLES:
        if style in name:
            name = name.replace(' '+style, '')
    return name


def get_macstyle(ttfont):
    bold, italic = fontdata.parse_metadata(ttfont)
    mac_style = (italic << 1) | bold
    return mac_style


def get_fsselection(ttfont):
    bold, italic = fontdata.parse_metadata(ttfont)
    fs_type = ((bold << 5) | italic) or (1 << 6)
    if italic:
        fs_type |= 1
    # check use_typo_metrics is enabled
    if 0b10000000 & ttfont['OS/2'].fsSelection:
        fs_type |= 128
    return fs_type


def parse_metadata(font):
        """Parse font name to infer weight and slope."""
        font_name = font_data.font_name(font)
        bold = 'Bold' in font_name.split()
        italic = 'Italic' in font_name.split()
        return bold, italic
