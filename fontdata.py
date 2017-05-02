from fontTools.ttLib import TTFont
import re

import gfspec


def get_familyname(ttfont):
    """Get the name of a font file"""
    name = ttfont['name'].getName(1, 3, 1, 1033).string
    name = name.decode('utf_16_be')
    for style in gfspec.STYLES:
        if style in name:
            name = name.replace(' '+style, '')
    return name


def is_canonical(filename):
    if '-' in filename:
        return True
    return False


def increment_version_number(ttfont, inc):
    """Increment a fonts version number.

    Update the name records and head.fontRevision.
    If a versions name records is badly formatted,
    create one from the head.fontRevision."""
    version_pattern = r'[0-9]{1,4}\.[0-9]{1,4}'
    name_table = ttfont['name']
    for name in name_table.names:

        if name.nameID in [3, 5]:
            enc = 'mac-roman' if name.langID == 0 else 'utf_16_be'
            record_text = name.string.decode(enc)

            version = re.search(version_pattern, record_text)

            if version:
                current_version = float(version.group())
                new_version = float(version.group()) + inc

                new_record_text = record_text.replace(
                    "%.3f" % current_version,
                    "%.3f" % new_version
                )
            else:
                new_version = float(ttfont['head'].fontRevision) + inc
                new_record_text = 'Version %.3f' % new_version

            name_table.setName(
                new_record_text.encode(enc),
                name.nameID,
                name.platformID,
                name.platEncID,
                name.langID,
            )

            ttfont['head'].fontRevision = new_version
