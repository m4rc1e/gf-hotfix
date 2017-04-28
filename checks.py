from nototools import font_data
from names import nametable_from_filename
import fontdata


def check_fsselection(ttfont):
    expected_fs_type = fontdata.get_fsselection(ttfont)
    print font_data.font_name(ttfont), ttfont['OS/2'].fsSelection, expected_fs_type
    return 'FAIL' if expected_fs_type != ttfont['OS/2'].fsSelection else 'PASS'


def check_macstyle(ttfont):
    """Check the macStyle bit"""
    expected_mac_style = fontdata.get_macstyle(ttfont)
    return 'FAIL' if ttfont['head'].macStyle != expected_mac_style else 'PASS'


def check_name_table(ttfont, font_path):
    nameids_to_check = [1, 2, 4, 6, 16, 17]
    passed = []
    nametable = ttfont['name']
    try:
        expected_nametable = nametable_from_filename(font_path)
    except:
        all
        return 'FAIL C'
    for field in nametable.names:
        name_id = field.nameID 
        if name_id in nameids_to_check:
            selected_field = (name_id, field.platformID, field.platEncID, field.langID)
            current_field = nametable.getName(*selected_field)
            expected_field = expected_nametable.getName(*selected_field)
            enc = current_field.getEncoding()

            if not expected_field:
                return 'FAIL'
            if str(current_field.string).decode(enc) != str(expected_field.string).decode(enc):
                passed.append('Fail')

    if 'FAIL' in passed:
        return 'FAIL'
    return 'PASS'


def check_fstype(ttfont):
    """fs type should be installable 0"""
    expected_fs_type = 0
    return 'FAIL' if ttfont['OS/2'].fsType != expected_fs_type else 'PASS'
