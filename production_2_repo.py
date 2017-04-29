"""
Convert the flat production font folder into a 
google/fonts repo.

Store fonts which do not a folder in the repo in a _todo dir
"""
import sys
import os
import shutil
from settings import production_fonts_dir, gf_api_url


TODO = '_todo'


def copy_repo_fonts_dir(root_path):
    if 'fonts' in root_path:
        print 'Removing old google/fonts folder'
        repo_cp_path = os.path.join('.', 'bin', 'repo_cp')
        if os.path.isdir(repo_cp_path):
            shutil.rmtree(repo_cp_path)
        print 'Copying specified google/fonts folder, be patient 1.5gb'
        shutil.copytree(root_path, repo_cp_path)
    else:
        print 'Path specified is not the fonts folder from fonts/google'


def main(root_path):
    copy_repo_fonts_dir(root_path)
    # build map of production files with realnames
    # build map of repo files
    # Iterate through repo files
        # if the repo is not in manual fonts, continue
        # if names match, swap production font with repo font



if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[-1])
    else:
        'please add google/fonts repo path'
