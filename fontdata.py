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


def parse_metadata(font):
        """Parse font name to infer weight and slope."""
        font_name = font_data.font_name(font)
        bold = 'Bold' in font_name.split()
        italic = 'Italic' in font_name.split()
        return bold, italic