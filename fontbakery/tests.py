from fontTools.ttLib import TTFont 

import utils
import gfspec

import unittest


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.font_files = utils.get_fonts('./bin')
        self.production_fonts = [TTFont(f) for f in self.font_files]

    def test_rebuild_font_filename(self):
        for font in self.production_fonts:
            self.assertIn('ttf', utils.rebuild_font_filename(font))


class TestGFSpec(unittest.TestCase):

    def test_get_fsselection(self):
        pass

    def test_macstyle(self):
        self.assertEqual(gfspec.get_macstyle('Family-Regular.ttf'), 0)
        self.assertEqual(gfspec.get_macstyle('Family-Italic.ttf'), 2)
        self.assertEqual(gfspec.get_macstyle('Family-Bold.ttf'), 1)
        self.assertEqual(gfspec.get_macstyle('Family-BoldItalic.ttf'), 3)

    def test_weightclass(self):
        self.assertEqual(gfspec.get_weightclass('Family-Thin.ttf'), 250)
        self.assertEqual(gfspec.get_weightclass('Family-ThinItalic.ttf'), 250)

        self.assertEqual(gfspec.get_weightclass('Family-Regular.ttf'), 400)
        self.assertEqual(gfspec.get_weightclass('Family-Italic.ttf'), 400)
        


if __name__ == '__main__':
    unittest.main()
