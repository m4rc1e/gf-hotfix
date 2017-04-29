
def get_familyname(ttfont):
    """Get the name of a font file"""
    name = ttfont['name'].getName(1, 3, 1, 1033).string
    name = name.decode('utf_16_be')
    for style in STYLES:
        if style in name:
            name = name.replace(' '+style, '')
    return name


def is_canonical(filename):
    if '-' in filename:
        return True
    return False
