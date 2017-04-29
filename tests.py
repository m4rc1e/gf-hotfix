from fontTools.ttLib import TTFont 

import utils
import unittest


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.font_files = utils.get_fonts('./bin')
        self.production_fonts = [TTFont(f) for f in self.font_files]

    def test_rebuild_font_filename(self):
        for font in self.production_fonts:
            self.assertIn('ttf', utils.rebuild_font_filename(font))


if __name__ == '__main__':
    unittest.main()
