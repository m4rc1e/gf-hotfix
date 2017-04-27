"""
Download all the fonts hosted on fonts.google.com
"""
import time
import os
import shutil
import json
import requests
from pprint import pprint
from settings import production_fonts_dir, gf_api_url




def get_gf_font_urls(gf_fonts):
    urls = []
    for item in gf_fonts['items']:
        for file in item['files']:
            urls.append(item['files'][file])
    return urls


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


def main():
    api_request = requests.get(gf_api_url)
    gf_fonts = json.loads(api_request.text)

    font_urls = get_gf_font_urls(gf_fonts)
    delete_files(production_fonts_dir)
    download_files(font_urls, production_fonts_dir)


if __name__ == '__main__':
    main()
