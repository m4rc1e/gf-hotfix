#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Client wrapper for the GF api which powers frontend of fonts.google.com.

Get font information and download the zipped families.
"""
import requests
import json
import os
from zipfile import ZipFile
import utils


API_PREFIX = 'http://fonts.google.com/metadata/fonts/'

DOWNLOAD_FAMILY_PREFIX = 'https://fonts.google.com/download?family='


class GFFont(object):
    """Download a family zip from fonts.google.com"""
    def __init__(self, name):
        self.name = name
        self._info = None
        self.zip = self._download_family()

    def _download_family(self):
        """Downloads a family .zip file from fonts.google.com"""
        if self._family_exists():
            dl_url = DOWNLOAD_FAMILY_PREFIX + self.name.replace(' ', '+')
            family_zip = utils.download_file(dl_url)
            return ZipFile(family_zip)
        return None

    def _family_exists(self):
        """Check if a font family exists on fonts.google.com"""
        url = self._family_url()
        request = requests.get(url)
        if request.status_code == 200:
            return True
        return False

    def _family_url(self):
        url_prefix = 'http://fonts.google.com/specimen/'
        dl_name = self.name.replace(' ', '+')
        return url_prefix + dl_name

    def download_license(self, dest=None):
        """Return the license file of an existing family. Save it to a
        destination if specified."""
        known_licenses = ['LICENSE.txt', 'OFL.txt', 'LICENCE.txt']

        for license in known_licenses:
            if license in self.zip.namelist():
                license_file = self.zip.open(license)

                if dest:
                    license_dest = os.path.join(dest, license)
                    with open(license_dest, 'w') as doc:
                        doc.write(license_file.read())
                else:
                    return license_file.read()

    def download_description(self, dest=None):
        family_info = family_api_info(self.name)
        text = family_info['description']
        if dest:
            dest_path = os.path.join(dest, 'DESCRIPTION.en_us.html')
            with open(dest_path, 'w') as doc:
                doc.write(text.encode('utf-8'))
        else:
            return text

    @property
    def info(self):
        if not self._info:
            self._info = family_api_info(self.name)
        return self._info


def family_api_info(name):
    """Get family information from the frontend GF api"""
    url = API_PREFIX + name.replace(' ', '+')
    request = requests.get(url)
    return json.loads(request.text[5:])


if __name__ == '__main__':

    rokkit = GFFont('Rokkitt')

    print rokkit.info['category']
    print rokkit.download_description()
