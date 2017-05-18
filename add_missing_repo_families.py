"""
Several families exist on fonts.google.com but don't have a family dir
in the google/fonts repository.
"""
import pandas as pd
import shutil
import os
import subprocess
from fontTools.ttLib import TTFont

from fontbakery.utils import (
    api_request,
    get_fonts,
    get_folder,
    delete_files,
)
from fontbakery.gffamily import GFFont, family_api_info
from fontbakery import fontdata
from fontbakery.fontdata import get_repo_name
from settings import (
    gf_api_url,
    production_fonts_fixed_dir,
    repo_missing_fonts,
    repo_cp_path
)
import blacklist


def families_2_add(report):
    """Families which exist on fonts.google but not in google/fonts"""
    repo_vs_prod = pd.read_csv(report, delimiter='\t')
    repo_missing_families = repo_vs_prod['google/fonts missing']
    # Filter out any fonts which are not on fonts.google.com
    api_families = [i['family'] for i in api_request(gf_api_url)['items']]
    return [f for f in repo_missing_families if f in api_families and
            f not in blacklist.existing_pr]


def get_families_directory(families):
    directories = []
    for family in families:
        family_dir = get_family_directory(family)
        directories.append(family_dir)
    return directories
        # break  # remove this later, lets test on just one family


def get_family_directory(family):
    """Return the path to a family, if it doesn't exist, build a directory
    for the family.

    Use the GF api to determine the correct license parent folder"""
    repo_name = get_repo_name(family)
    family_dir = get_folder(repo_missing_fonts, repo_name)
    if family_dir:
        return family_dir

    print 'Creating folder for %s' % family
    family_data = family_api_info(family)
    license_type = family_data['license']
    
    # Make the parent directory if it doesn't exist
    parent_dir = os.path.join(repo_missing_fonts, license_type)
    if not os.path.isdir(parent_dir):
        os.mkdir(parent_dir)

    #Make the family directory if it doesn't exist
    family_dir = os.path.join(parent_dir, repo_name)
    if not os.path.isdir(family_dir):
        os.mkdir(family_dir)
    return family_dir



def move_fonts_2_directories(fonts, directories):
    """Move fonts to their target family directories"""
    directories = {get_repo_name(d): d for d in directories}
    for font_path in fonts:
        folder_name = get_repo_name(font_path)
        if folder_name in directories:
            print 'Copying %s to %s' % (font_path, directories[folder_name])
            shutil.copy(font_path, directories[folder_name])


def name_from_font_path(path):
    """Get the folders fony family name"""
    fonts = get_fonts(path)
    ttfont = TTFont(fonts[0])
    return fontdata.get_familyname(ttfont)


def get_previous_families_data(directories):
    """Add the following data from the api:

    1. The license file from the family hosted on fonts.google.com
    2. The DESCRIPTION.en_us.html from the hosted family
    3. Update the METADATA.pb files to include previous info.
 
    """
    for directory in directories:
        family_name = name_from_font_path(directory)
        if not family_name.endswith(' '):
            old_family = GFFont(family_name)

            print "Saving license file for %s" % directory
            old_family.download_license(directory)

            print "Updating DESCRIPTION.en_us.html for %s" % directory
            old_family.download_description(directory)

            print "Updating METADATA.pb for %s" % directory
            update_metadata(directory, old_family.info)


def update_metadata(directory, family_api_json):
    """Replace the placeholders with data from the api"""
    metadata_file = os.path.join(directory, 'METADATA.pb')
    metadata = []
    with open(metadata_file, 'r') as doc:
        metadata = doc.readlines()

    # inherit old designers
    old_designers = [d['name'] for d in family_api_json['designers']]
    metadata[1] = 'designer: "%s"\n' % ', '.join(old_designers)
    # inherit old category
    old_category = family_api_json['category'].upper().replace(' ', '_')
    metadata[3] = 'category: "%s"\n' % old_category
    # inherit old date
    metadata[4] = 'date_added: "%s"\n' % family_api_json['lastModified']

    with open(metadata_file, 'w') as doc:
        text = ''.join(metadata).encode('utf-8')
        text = text.replace('\\r\\n', ' ')
        text = text.replace('\\n\\r', ' ')
        text = text.replace('\\r', ' ')
        text = text.replace('\\n', ' ')
        doc.write(''.join(metadata).encode('utf-8'))


def generate_families_metadata(directories):
    """Generate METADATA.pb files using add_font.py --update"""
    c_dir = os.getcwd()
    os.chdir(os.path.join(repo_cp_path, 'tools'))

    for directory in directories:
        print 'Generating metadata for %s' % directory
        subprocess.call(['python', 'add_font.py', directory])
    os.chdir(c_dir)


def main():
    if not os.path.isdir(repo_missing_fonts):
        os.mkdir(repo_missing_fonts)
    delete_files(repo_missing_fonts)
    families = families_2_add('./reports/repo_vs_production.csv')
    fixed_fonts = get_fonts(production_fonts_fixed_dir)
    directories = get_families_directory(families)
    move_fonts_2_directories(fixed_fonts, directories)
    generate_families_metadata(directories)
    get_previous_families_data(directories)


if __name__ == '__main__':
    main()
