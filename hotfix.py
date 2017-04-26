#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Collection wide hotfix script"""
import os
import csv
import sys
import logging
from ntpath import basename
from fontTools.ttLib import TTFont
import checks
from fbchecklogger import FontBakeryCheckLogger
from targetfont import TargetFont
from constants import YELLOW_STR,\
                      GREEN_STR,\
                      BLUE_STR,\
                      RED_STR,\
                      WHITE_STR,\
                      CYAN_STR,\
                      NORMAL
import pandas as pd

log_config = {
    'files': ['/'],
    'autofix': 0,
    'verbose': 0,
    'json': False,
    'ghm': False,
    'error': '-e',
    'inmem': False,
    'webapp': False
  }

IGNORE_FAMILIES = []


class FontBakeryCheckLogger2(FontBakeryCheckLogger):
    # pass
    def flush(self):
        if self.current_check:
            self.update_progressbar()
            self.all_checks.append(self.current_check)

    def new_check(self, check_number, desc):
        logging.debug("Check #{}: {}".format(check_number, desc))
        self.current_check = {"description": desc,
                              "checkx_number": check_number,
                              "log_messages": [],
                              "result": "unknown",
                              "priority": NORMAL,
                              "target": self.default_target}
        self.flush()


def get_families(root_path):
    families = []
    for path, r, files in os.walk(root_path):
        if basename(path) not in IGNORE_FAMILIES:
            family = [os.path.join(path, f) for f in files if f.endswith('.ttf')]
        if family:
            families.append(family)
    return families


def make_target_family(family):
    fonts_to_check = []
    for path in family:
        if '-' in path:
            a_target = TargetFont()
            a_target.fullpath = path
            a_target.get_ttfont()  # should just be part of font.ttfont attrib
            fonts_to_check.append(a_target)
    return fonts_to_check


def check_fsselection(fb, font, style):
    fb.new_check("1000", "fsSelection 2")

    bits = 0
    if 'Regular' in style:
        bits |= 0b1000000
    else:
        bits &= ~0b1000000
    if 'Bold' in style:
        bits |= 0b100000
    else:
        bits &= ~0b100000
    if 'Italic' in style:
        bits |= 0b1
    else:
        bits &= ~0b1
  
    try:
        if bits == font['OS/2'].fsSelection:
            fb.ok('fsSelection is correct')
            return
        fb.error('fsSelection is incorrect')
        return
    except:
        all 
        fb.error('fucked')



def check_mac_style(fb, font, style):
    fb.ok('dummy pass')



def main(fonts_paths):

    families = get_families(fonts_paths)
    # families = get_families('/Users/marc/Documents/googlefonts/fonts/ofl/montserrat')
    loggers = []
    failed_fonts = []

    for family in families:
        
        fonts_to_check = make_target_family(family)

        for target in fonts_to_check:
            logger = FontBakeryCheckLogger2(config=log_config)

            family_files = fonts_to_check
            logger.set_font(target.ttfont)

            # checks.check_files_are_named_canonically(logger, fonts_to_check)

            # checks.check_font_version_fields(logger, target.ttfont) BROKEN
            # checks.check_all_fontfiles_have_same_version(logger, family_files)

            # checks.check_fullfontname_begins_with_the_font_familyname(logger, target.ttfont)


            check_fsselection(logger, target.ttfont, target.style)
            # check_mac_style(logger, target.ttfont, target.style)
            # checks.check_OS2_usWeightClass(logger, target.ttfont, target.style)
            # checks.check_fsSelection_REGULAR_bit(logger, target.ttfont, target.style)
            # checks.check_fsSelection_ITALIC_bit(logger, target.ttfont, target.style)
            # checks.check_macStyle_ITALIC_bit(logger, target.ttfont, target.style)
            # checks.check_fsSelection_BOLD_bit(logger, target.ttfont, target.style)
            # checks.check_macStyle_BOLD_bit(logger, target.ttfont, target.style)
            # checks.check_for_unwanted_tables(logger, target.ttfont)

            # checks.check_Digital_Signature_exists(logger, target.ttfont, target.fullpath)

            # checks.check_GASP_table_is_correctly_set(logger, target.ttfont)


            # checks.check_OS2_fsType(logger)
            # checks.check_main_entries_in_the_name_table(logger, target.ttfont, target.fullpath) BROKEN


            loggers.append(logger)




    # generate a csv from a pivoted dataframe
    table = []
    for logger in loggers:
        for check in logger.all_checks:
            table.append([
                str(logger.font['name'].getName(4, 3, 1, 1033)).decode('utf_16_be'),
                check['description'],
                check['result'].encode('utf-8')
            ])



    df = pd.DataFrame(table, columns=['font', 'test', 'status'])
    df = df.drop_duplicates()
    df.to_csv('prepivot.csv', sep='\t', encoding='utf-8')
    df = df.pivot(index='font', columns='test', values='status')
    df.to_csv('frank.csv', sep='\t', encoding='utf-8')

    print len(set(failed_fonts)), failed_fonts



if __name__ == '__main__':
    main(sys.argv[-1])
