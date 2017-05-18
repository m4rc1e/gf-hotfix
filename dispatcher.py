"""
PR fonts from rebuilt repo tree into google/fonts main repo


script sequence:

Map copied repo family paths to real repo family paths

For family in fixed_families:
    copy over family to real repo
    create a a new branch and pr the new family, if the
    family hasn't been prd yet.

"""
import os
import git
from ntpath import basename
from fontTools.ttLib import TTFont
import shutil
import subprocess
from argparse import ArgumentParser

from settings import repo_cp_path, sprint1_start
from fontbakery import fontdata
from fontbakery.utils import get_fonts, get_folders
from fontbakery.gfcollection import Repository


def pr_family(src_path, dest_path):
    """Replace a family and do git operations to submit pr for family to
    google/fonts"""

    c_dir = os.getcwd()
    print 'Replacing %s' % dest_path

    try:
        shutil.rmtree(dest_path)
    except OSError:
        print 'Family does not exist, adding instead'
    shutil.copytree(src_path, dest_path)

    os.chdir(dest_path)
    folder = basename(dest_path)

    # git initialisation operations
    repo = git.Git('.')
    repo.checkout('master')
    # repo.pull('origin master') # update our master to match google/fonts

    branch_name = 'hotfix-%s' % folder
    repo.checkout('HEAD', b=branch_name)
    
    repo.add('../%s' % folder)
    repo_fonts_paths = get_fonts(os.path.join(c_dir, src_path))
    fam_version = fontdata.get_version(TTFont(repo_fonts_paths[0]))
    commit_msg = '%s: v%s added' % (branch_name, fam_version)
    repo.commit('-m', commit_msg)
    repo.push('upstream')
    
    # git make pr
    print 'PRing to google/fonts'
    subprocess.call(['hub', 'pull-request', '-b', 'google/fonts:master', '-m', commit_msg])

    # rest git and go back to c_dir
    repo.checkout('master')
    os.chdir(c_dir)


def pr_families(user_paths, dest_paths):
    for user_path, dest_path in zip(user_paths, dest_paths):
        pr_family(user_path, dest_path)


def create_missing_dest_paths(repo_path, user_dirs, dest_dirs):
    """If a destination directory does not exist, create a path for it"""
    dirs = []
    for user_dir, dest_dir in zip(user_dirs, dest_dirs):
        if not dest_dir:
            dest_dir = repo_path + user_dir.replace(repo_cp_path, '')
        dirs.append(dest_dir)
    return dirs


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("repo_path",
                        help="Path to local git linked google/fonts repo")
    parser.add_argument("git_username")
    parser.add_argument("git_password")
    parser.add_argument("families", nargs='+',
                        help="family folders to batch pr")
    args = parser.parse_args()

    repo = Repository(args.git_username, args.git_password)
    already_dispatched = repo.families_pr_after(sprint1_start)
    already_dispatched_dir = [fontdata.get_repo_name(f) for f in already_dispatched]
    families_2_dispatch = set(args.families) - set(already_dispatched_dir)

    if families_2_dispatch:
        user_dirs = get_folders(repo_cp_path, families_2_dispatch)
        dest_dirs = get_folders(args.repo_path, families_2_dispatch)
        dest_dirs = create_missing_dest_paths(args.repo_path, user_dirs, dest_dirs)
        pr_families(user_dirs, dest_dirs)
    
    for family in args.families:
        if family in already_dispatched_dir:
            print 'WARNING: %s has already dispatched, skipping.' % family

        
if __name__ == '__main__':
    main()
