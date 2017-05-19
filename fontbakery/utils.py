"""
Module of useful helper functions to manipulate files/folders.
"""
import requests
import shutil
import hashlib
import os
import json
from ntpath import basename
from StringIO import StringIO


def get_fonts(root_path, filetype='.ttf'):
    fonts = []
    for path, r, files in os.walk(root_path):
        for f in files:
            if f.endswith(filetype):
                fonts.append(os.path.join(path, f))
    return fonts


def get_folders(root_path, folders_name):
    folders = []
    for folder_name in folders_name:
        folder = get_folder(root_path, folder_name)
        folders.append(folder)
    return folders


def get_folder(root_path, folder_name):
    """Return the path to a folder if the folder exists in the
    root path tree"""
    for path, r, files in os.walk(root_path):
        if basename(path) == folder_name:
            return path
    return None


def hash_files(files):
    hashes = {}
    for f in files:
        checksum = hash_file(f)
        hashes[checksum] = f
    return hashes


def hash_file(f):
    checksum = hashlib.md5(open(f, 'rb').read()).hexdigest()
    return checksum


def download_files(urls, dest):
    for url in urls:
        download_file(url, dest)


def api_request(url):
    """Return json from an api get endpoint"""
    api_request = requests.get(url)
    return json.loads(api_request.text)


def download_file(url, dest=None, log=True):
    """Download a file from a url to a specified destination.
    If no location is given, store file in memory as a
    StringIO object.

    Implementation handles larger files by breaking them down
    into chunks."""
    filename = os.path.basename(url)
    r = requests.get(url, stream=True)
    if log:
        print 'Downloading %s to %s' % (url, dest)
    if dest:
        with open(os.path.join(dest, filename), 'w') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
    else:
        s = StringIO()
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                s.write(chunk)
        return s


def delete_files(directory):
    shutil.rmtree(directory)
    os.makedirs(directory)


def rebuild_font_filename(ttfont):
    """Recreate a font's filename from the ps name"""
    ps_name = ttfont['name'].getName(6, 3, 1, 1033).string.decode('utf_16_be')
    return ps_name + '.ttf'
