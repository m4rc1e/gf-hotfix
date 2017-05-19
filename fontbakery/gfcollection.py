"""
Wrapper for the production server api and git repository
"""
from datetime import datetime
from github import Github
import os

from utils import api_request
from fontdata import familyname_from_filename


gf_api_url = 'http://tinyurl.com/m8o9k39'


class ProductionServer:
    """Client wrapper for Google Fonts api"""
    def __init__(self):
        self.api_data = api_request(gf_api_url)

    def modified_after(self, date):
        """Return families which have been modified after a certain date"""
        families = []
        for item in self.api_data['items']:
            item_date = self._parse_date(item['lastModified'])
            date_t = self._parse_date(date)
            if item_date >= date_t:
                families.append(item)
        return families

    @staticmethod
    def _parse_date(date):
        """Parse string date YYYY-MM-DD into datetime object"""
        date_parsed = tuple(map(int, date.split('-')))
        return datetime(*date_parsed)

    @property
    def family_count(self):
        return len([f for f in self.api_data['items']])


class Repository:
    """Client wrapper for google/fonts repository"""
    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.git = Github(username, password)
        self.user = self.git.get_user('google')
        self.repo = self.user.get_repo('fonts')        

    def families_merged_after(self, date):
        """Return families which have been merged"""
        families = set()
        print 'Analysing pull requests, be patient'
        request_date = ProductionServer._parse_date(date)
        for pull in self.repo.get_pulls('closed'):
            if pull.merged and pull.created_at >= request_date:
                self._get_families(families, pull)
        return families

    def families_unmerged_after(self, date):
        """Return families which have open pull requests"""
        families = set()
        print 'Analysing pull requests, be patient'
        request_date = ProductionServer._parse_date(date)
        for pull in self.repo.get_pulls():
            if pull.created_at >= request_date:
                self._get_families(families, pull)
        return families

    def families_pr_after(self, date):
        """Return all families which may have open or merged prs"""
        merged = self.families_merged_after(date)
        unmerged = self.families_unmerged_after(date)
        return merged | unmerged

    def _get_families(self, families, pull):
        """Check which families have been touched in the pr"""
        for f in pull.get_files():
            font_filename = os.path.basename(f.filename)
            if '.ttf' in font_filename:
                family = familyname_from_filename(font_filename)
                families.add(family)
