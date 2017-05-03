#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Package fixed fonts into duplicate GF repo
"""
import os
import sys
import re
import shutil
from ntpath import basename
import subprocess

from utils import api_request, get_fonts
from settings import gf_api_url, production_fonts_fixed_dir, repo_cp_path
from gfcollection import get_repo_name


def copy_repo_fonts_dir(root_path, repo_cp_path):
    if 'fonts' in root_path:
        print 'Removing old google/fonts folder'
        if os.path.isdir(repo_cp_path):
            shutil.rmtree(repo_cp_path)
        print 'Copying specified google/fonts folder, be patient 1.5gb'
        shutil.copytree(root_path, repo_cp_path)
    else:
        print 'Path specified is not the fonts folder from fonts/google'


def get_families_codepages(gf_api_json):
    codepages = {}
    for item in gf_api_json['items']:
        codepages[item['family']] = item['subsets']

        if 'menu' not in codepages[item['family']]:
            codepages[item['family']].append('menu')

        codepages[item['family']] = sorted(codepages[item['family']])
    return codepages


def delete_repo_fonts(gf_repo_path, families_2_update):
    """Delete ttf font files for specific folders"""
    for path, r, files in os.walk(gf_repo_path):
        if basename(path) in families_2_update:
            for f in files:
                if f.endswith('.ttf'):
                    font = os.path.join(path, f)
                    os.remove(font)


def add_repo_fonts(gf_repo_path, fonts_2_package, families_2_update):
    f = {}
    for path in fonts_2_package:
        pkg_name = get_repo_name(path)
        if not pkg_name in f:
            f[pkg_name] = []
        f[pkg_name].append(path)

    for to_path, r, files in os.walk(gf_repo_path):
        current_folder = basename(to_path)
        if current_folder in families_2_update:
            for from_path in f[current_folder]:
                shutil.copy(from_path, to_path)


def swap_repo_fonts(fonts_2_package, gf_repo_path, families_2_update):
    """swap the fixes fonts into a gf repo"""
    delete_repo_fonts(gf_repo_path, families_2_update)
    add_repo_fonts(gf_repo_path, fonts_2_package, families_2_update)


def update_family_metadata_file(path, families_codepages, gen_metadata_script):
    path = os.path.join(os.getcwd(), path)
    metadata_path = os.path.join(path, 'METADATA.pb')

    if os.path.exists(metadata_path):

        metadata_dup = metadata_path + '.cp'
        shutil.copy(metadata_path, metadata_dup)

        new_metadata = []
        with open(metadata_dup, 'r') as meta:
            meta = meta.readlines()[:5]
            for item in meta:
                new_metadata.append(item.decode('utf-8'))

        c_dir = os.getcwd()
        os.chdir(os.path.dirname(gen_metadata_script))
        # generate a new METADATA.pb file
        subprocess.call(['python', 'add_font.py', path])
        os.chdir(c_dir)

        with open(metadata_path, 'r') as genned_metadata:
            meta_text = genned_metadata.read()
            fonts_records = re.findall(r'fonts \{.*\}', meta_text, re.MULTILINE|re.DOTALL)
            for font_record in fonts_records:
                new_metadata.append(font_record + '\n')

            fam_name = new_metadata[0][7:-2]
            for subset in families_codepages[fam_name]:
                new_metadata.append('subsets: "%s"\n' % subset.lower())

        with open(metadata_path, 'w') as regenned_metadata:
            text = ''.join(new_metadata).encode('utf-8')
            regenned_metadata.write(text)

        os.remove(metadata_dup)


def update_families_metadata_pb(gf_repo_path, families_codepages, families_2_update, gen_metadata_script):
    for path, r, files in os.walk(gf_repo_path):
        if basename(path) in families_2_update:
            update_family_metadata_file(path, families_codepages, gen_metadata_script)


def main(gen_metadata_script):
    gf_repo_path = '/Users/marc/Documents/googlefonts/fonts'
    copy_repo_fonts_dir(gf_repo_path, repo_cp_path)
    fonts_2_package = get_fonts(production_fonts_fixed_dir)
    families_2_update = set([get_repo_name(f) for f in fonts_2_package])
    print 'Replacing broken fonts with fixed fonts'
    swap_repo_fonts(fonts_2_package, repo_cp_path, families_2_update)
    gf_collection = api_request(gf_api_url)
    families_codepages = get_families_codepages(gf_collection)
    print 'Updating family METADATA.pb files'
    update_families_metadata_pb(repo_cp_path, families_codepages, families_2_update, gen_metadata_script)
 

if __name__ == '__main__':
    # meta_script = '/Users/marc/Documents/googlefonts/fonts/tools/add_font.py'
    # gf_tools = os.path.dirname(meta_script)
    # os.chdir(gf_tools)
    # p = '/Users/marc/Documents/googlefonts/hotfix/bin/repo_cp/ofl/acme'
    # code_p = {'Acme': ['vietnamese', 'menu', 'latin', 'latin-ext']}
    # update_family_metadata_file(p, code_p, meta_script)

    if len(sys.argv) != 2:
        print 'Add path to add_font.py script'
    else:
        main(sys.argv[-1])
