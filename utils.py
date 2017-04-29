import requests
import shutil
import hashlib
import os

def get_fonts(root_path):
    fonts = []
    for path, r, files in os.walk(root_path):
        for f in files:
            if f.endswith('.ttf'):
                fonts.append(os.path.join(path, f))
    return fonts


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


def download_file(url, dest, log=True):
    """Download a file from a url to a specified destination.

    Implementation handles larger files by breaking them down
    into chunks."""
    filename = os.path.basename(url)
    r = requests.get(url, stream=True)
    if log:
        print 'Downloading %s to %s' % (url, dest)
    with open(os.path.join(dest, filename), 'w') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


def delete_files(directory):
    shutil.rmtree(directory)
    os.makedirs(directory)


def rebuild_font_filename(ttfont):
    """Recreate a font's filename from the ps name"""
    ps_name = ttfont['name'].getName(6, 3, 1, 1033).string.decode('utf_16_be')
    return ps_name + '.ttf'
