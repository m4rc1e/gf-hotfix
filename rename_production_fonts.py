"""
Convert the flat production font folder into a 
google/fonts repo.

Store fonts which do not a folder in the repo in a _todo dir
"""
import sys
import os
import shutil
from ntpath import basename
from settings import production_fonts_dir, production_fonts_renamed_dir, gf_api_url
from utils import api_request, delete_files


API_2_STYLENAMES = {
    "100": "Thin",
    "100italic": "ThinItalic",
    "200": "ExtraLight",
    "200italic": "ExtraLightItalic",
    "300": "Light",
    "300italic": "LightItalic",
    "regular": "Regular",
    "italic": "Italic",
    "500": "Medium",
    "500italic": "MediumItalic",
    "600": "SemiBold",
    "600italic": "SemiBoldItalic",
    "700": "Bold",
    "700italic": "BoldItalic",
    "800": "ExtraBold",
    "800italic": "ExtraBoldItalic",
    "900": "Black",
    "900italic": "BlackItalic",
}


def production_fontnames_2_real(gf_api_request):
    """list of tuples containing the hashed fontname and the generated real
    name"""
    n = []
    for item in gf_api_request['items']:
        for style in item['files']:
            realname = '%s-%s.ttf' % (
                item['family'].replace(' ', ''),
                API_2_STYLENAMES[style]
            )
            n.append((basename(item['files'][style]), realname))
    return n


def rename_production_fonts_2_realnames(src_dir, out_dir, names):
    for src_name, out_name in names:
        hashed_font_path = os.path.join(src_dir, src_name)
        real_font_path = os.path.join(out_dir, out_name)
        shutil.copy(hashed_font_path, real_font_path)


def main():
    gf_api_request = api_request(gf_api_url)
    if not os.path.isdir(production_fonts_renamed_dir):
        os.mkdir(production_fonts_renamed_dir)
    delete_files(production_fonts_renamed_dir)
    fontnames = production_fontnames_2_real(gf_api_request)
    rename_production_fonts_2_realnames(production_fonts_dir, production_fonts_renamed_dir, fontnames)


if __name__ == '__main__':
    main()
