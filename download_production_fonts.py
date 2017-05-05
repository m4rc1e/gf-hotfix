"""
Download all the fonts hosted on fonts.google.com
"""
import os
import json
import requests
from settings import production_fonts_dir, gf_api_url
from utils import download_files, delete_files, api_request


def get_gf_font_urls(gf_fonts):
    urls = []
    for item in gf_fonts['items']:
        for file in item['files']:
            urls.append(item['files'][file])
    return urls


def main():
    gf_api_request = api_request(gf_api_url)
    font_urls = get_gf_font_urls(gf_api_request)
    if not os.path.isdir('out'):
        os.mkdir('out')
        os.mkdir(production_fonts_dir)
    delete_files(production_fonts_dir)
    download_files(font_urls, production_fonts_dir)


if __name__ == '__main__':
    main()
