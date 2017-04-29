import re
from fontTools.ttLib import TTFont

import fontdata
import utils


NON_UNICASE_NAMES = [
    'IM FELL Great Primer',
    'Biryani UltraLight',
    'CantoraOne',
    'IM FELL Double Pica SC',
    'IM FELL Great Primer SC',
    'UnifrakturMaguntia',
    'Playfair Display SC',
    'PT Serif Caption',
    'NTR',
    'Montserrat Alternates ExLight',
    'Diplomata SC',
    'McLaren',
    'OdorMeanChey',
    'PT Sans',
    'VT323',
    'GFS Didot',
    'IM FELL French Canon',
    'Press Start 2P',
    'BenchNine',
    'Martel UltraLight',
    'BioRhyme',
    'Mate SC',
    'SirinStencil',
    'Cormorant SC',
    'IM FELL English',
    'IM FELL DW Pica SC',
    'HammersmithOne',
    'Old Standard TT',
    'NovaMono',
    'Amatic SC',
    'Almendra SC',
    'BioRhyme Expanded',
    'Biryani DemiBold',
    'IM FELL Double Pica',
    'PT Sans Caption',
    'Martel DemiBold',
    'IM FELL English SC',
    'Holtwood One SC',
    'EB Garamond',
    'Carrois Gothic SC',
    'GFS Neohellenic',
    'PT Sans Narrow',
    'Marcellus SC',
    'IM FELL DW Pica',
    'Amatica SC',
    'Overlock SC',
    'MedievalSharp',
    'PT Serif',
    'IM FELL French Canon SC',
    'UnifrakturCook',
    'Patrick Hand SC',
    'PT Mono',
    'HeadlandOne',
    'ABeeZee',
    'Bowlby One SC',
    'Alegreya Sans SC',
    'Alegreya SC',
    'Exo 2',
    'Mountains of Christmas',
    
]


if __name__ == '__main__':
    # Get NON_UNICASE_NAMES
    prod_fonts = utils.get_fonts('./bin')
    font_names = [fontdata.get_familyname(TTFont(p)) for p in prod_fonts]

    for name in set(font_names):
        if re.search(r"(?<=\w)([A-Z])", name):
            print "'%s'," % name