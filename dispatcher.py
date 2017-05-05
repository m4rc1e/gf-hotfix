"""
PR fonts from rebuilt repo tree into google/fonts main repo


script sequence:

Map copied repo family paths to real repo family paths
For family in fixed_families:
    copy over family to real repo
    create a a new branch and pr the new family

Warning: This is dangerous and will definately annoy people. I'm
setting a chunk limit so we can only pr a selected amount of
families each day.

"""
import sys
import os
import git
from datetime import datetime
from ntpath import basename
from fontTools.ttLib import TTFont
import shutil
import subprocess

from settings import repo_cp_path
from fontbakery import fontdata
from fontbakery.utils import get_fonts


DAILY_CHUNK = 100  # how many families to pr when running script


def parse_cmdln_date(d):
    d = d.split('/')
    d = map(int, d)
    d = tuple(d)
    return datetime(*d)


def families_dispatched(log_file):
    with open(log_file, 'r') as log:
        return log.read().splitlines()


def get_family_dirs(repo_path):
    repo_dirs_name = [basename(os.path.dirname(p)) for p in get_fonts(repo_path)]
    repo_dirs_paths = [os.path.dirname(p) for p in get_fonts(repo_path)]
    return dict(zip(repo_dirs_name, repo_dirs_paths))


def remove_dispatched_families(dirs, already_dispatched, usr_date):
    cleaned = {}
    for family_name, path in dirs.items():
        family_modified_thresh = parse_cmdln_date(usr_date)
        family_modified_date = datetime.fromtimestamp(os.path.getmtime(path))

        if family_modified_date >= family_modified_thresh:
            if family_name not in already_dispatched:
                cleaned[family_name] = path
    return cleaned


def get_swap_family_paths(dirs_2_dispatch, repo_dirs, limit=None):
    shared_dirs = set(dirs_2_dispatch) & set(repo_dirs)
    swap_families = []
    for folder in shared_dirs:
        swap_families.append((dirs_2_dispatch[folder], repo_dirs[folder]))
    swap_families = sorted(swap_families)
    if limit:
        return zip(*swap_families[:limit])
    return zip(*swap_families)


def replace_family(src_path, dest_path):
    """Replace a family and do git operations to submit pr for family to
    google/fonts"""

    c_dir = os.getcwd()
    print 'Replacing %s' % dest_path

    shutil.rmtree(dest_path)
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
    print repo_fonts_paths
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


def replace_families(src_paths, dest_paths):
    for src_path, dest_path in zip(src_paths, dest_paths):
        replace_family(src_path, dest_path)


def log_replaced_families(log_file, families):
    with open(log_file, 'a') as log:
        log.write('\n'.join(families))
        log.write('\n')


def main(repo_path, usr_date):
    already_dispatched = families_dispatched("dispatched_log.txt")
    source_repo_dirs = get_family_dirs(repo_path)
    cp_repo_dirs = get_family_dirs(repo_cp_path)
    dirs_2_dispatch = remove_dispatched_families(cp_repo_dirs, already_dispatched, usr_date)
    src_families, dest_families = get_swap_family_paths(dirs_2_dispatch, source_repo_dirs, limit=DAILY_CHUNK)
    replace_families(src_families, dest_families)
    replaced_families = [basename(p) for p in src_families]
    log_replaced_families("dispatched_log.txt", replaced_families)

        
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'please include path to ofl folder and date in format YYYY/MM/DD for folder to move'
    else:
        main(sys.argv[1], sys.argv[2])
