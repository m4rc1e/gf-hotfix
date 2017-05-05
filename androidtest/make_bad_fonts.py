"""
Generate a set of bad fonts from the good fonts.
"""
from fontTools.ttLib import TTFont
import os

for font_path in os.listdir('good_fonts'):
    if font_path.endswith('.ttf'):
        font = TTFont(os.path.join('good_fonts', font_path))
        font['OS/2'].fsSelection = 64  # set everything to Regular
        font['head'].macStyle = 0 # set everything to Bold
        font.save(os.path.join('bad_fonts', font_path))
        print 'bad font generated %s' % os.path.join('bad_fonts', font_path)