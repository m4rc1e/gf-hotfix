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

