"""
Module to help generate/update METADATA.pb files in google/fonts
"""
import os
import subprocess
from google.protobuf import text_format

import gffamily
import fonts_public_pb2 as fonts_pb2


def gen_metadata_4_missing_repo_family(script, family_folder, replace_codepages=False):
    """Generate a METADATA.pb file for families which exist on
    fonts.google.com but are not in the google/fonts repo"""
    family_path = os.path.join(os.getcwd(), family_folder)
    script_path = os.path.dirname(script)
    
    # Generate a fresh METADATA.pb file
    os.chdir(script_path)
    subprocess.call(['python', 'add_font.py', family_path])
    os.chdir(c_dir)

    # Repopulate genned metadata file with existing data from gf api
    metadata_file = os.path.join(family_path, 'METADATA.pb')
    metadata = fonts_pb2.FamilyProto()
    
    # f = open(metadata_file, 'rb')
    # g = f.read()
    # meta_data_struct.ParseFromString(g)
    # f.close()

    


    # family_meta = gffamily.get_info('Rokkitt')
    # # Add the license type
    # print family_meta['license']
    # # Add the designers
    # print [d['name'] for d in family_meta['designers']]
    # # Add codepages
    # print family_meta['coverage'].keys()
    # # last modified date
    # print family_meta['lastModified']


def metadata_4_missing(family_folder):

    metadata = fonts_pb2.FamilyProto()
    metadata.name = 'foobar'
    metadata.designer = 'Unknown'
  metadata.category = 'SANS_SERIF'
  metadata.license = font_license
  subsets = sorted(subsets)
  for subset in subsets:
    metadata.subsets.append(subset)
  metadata.date_added = time.strftime('%Y-%m-%d')

if __name__ == '__main__':
    gen_metadata_4_missing_repo_family(
        '/Users/marc/Documents/googlefonts/hotfix/out/repo_cp/tools/add_font.py',
        '/Users/marc/Downloads/ofl/biorhythm'
    )