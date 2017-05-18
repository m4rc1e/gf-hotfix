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

from fontbakery.utils import api_request, get_fonts
from settings import (
    gf_api_url,
    production_fonts_fixed_dir,
    repo_url,
    repo_cp_path,
    description_dir
)
from fontbakery.fontdata import get_repo_name


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


def update_family_metadata_file(path, families_codepages):
    path = os.path.join(os.getcwd(), path)
    metadata_path = os.path.join(path, 'METADATA.pb')

    if os.path.exists(metadata_path):

        metadata_dup = metadata_path + '.cp'
        shutil.copy(metadata_path, metadata_dup)

        new_metadata = []
        with open(metadata_dup, 'r') as meta:
            meta = meta.readlines()[:5]
            for item in meta:
                new_metadata.append(str(item))

        c_dir = os.getcwd()
        os.chdir(os.path.join(repo_cp_path, 'tools'))
        # generate a new METADATA.pb file.
        # Script only works from the same directory
        subprocess.call(['python', 'add_font.py', path])
        os.chdir(c_dir)

        with open(metadata_path, 'r') as genned_metadata:
            meta_text = genned_metadata.read()
            fonts_records = re.findall(r'fonts \{.*\}', meta_text, re.MULTILINE|re.DOTALL)
            for font_record in fonts_records:
                new_metadata.append(str(font_record + '\n'))

            fam_name = new_metadata[0][7:-2]
            # subsets are taken from api instead of METADATA.pb.
            # We should not be adding new ones
            for subset in families_codepages[fam_name]:
                new_metadata.append(str('subsets: "%s"\n' % subset.lower()))

        with open(metadata_path, 'w') as regenned_metadata:
            text = ''.join(new_metadata)
            text = text.replace('\\r\\n', ' ')
            text = text.replace('\\n\\r', ' ')
            text = text.replace('\\r', ' ')
            text = text.replace('\\n', ' ')
            regenned_metadata.write(text) 
        os.remove(metadata_dup)


def update_families_metadata_pb(gf_repo_path, families_codepages, families_2_update):
    for path, r, files in os.walk(gf_repo_path):
        if basename(path) in families_2_update:
            print 'updating meta for %s' % path
            update_family_metadata_file(path, families_codepages)


def replace_families_description_file(repo_cp_path, description_files, families_2_update):
    src_descs = {basename(os.path.dirname(f)): f for f in description_files}

    for path, r, files in os.walk(repo_cp_path):
        folder = basename(path)
        if folder in families_2_update:
            dest_description_file = os.path.join(path, 'DESCRIPTION.en_us.html')
            if os.path.isfile(dest_description_file):
                os.remove(dest_description_file)
                shutil.copy(src_descs[folder], dest_description_file)


def main():
    print 'cloning google/fonts'
    if os.path.isdir(repo_cp_path):
        shutil.rmtree(repo_cp_path)
    subprocess.call(['git', 'clone', repo_url, repo_cp_path])

    print 'Replacing broken fonts with fixed fonts'
    fonts_2_package = get_fonts(production_fonts_fixed_dir)
    families_2_update = set([get_repo_name(f) for f in fonts_2_package])
    swap_repo_fonts(fonts_2_package, repo_cp_path, families_2_update)

    print 'Updating family METADATA.pb files'
    gf_collection = api_request(gf_api_url)
    families_codepages = get_families_codepages(gf_collection)
    update_families_metadata_pb(repo_cp_path, families_codepages, families_2_update)

    print 'Replacing DESCRIPTION.en_us.html files'
    description_files = get_fonts(description_dir, filetype='.html')
    replace_families_description_file(repo_cp_path, description_files, families_2_update)
 

if __name__ == '__main__':
    main()
