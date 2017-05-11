import re
import requests
from fontTools.ttLib import TTFont
from zipfile import ZipFile
from StringIO import StringIO
import fontdata
import utils
from ntpath import basename



DOWNLOAD_FAMILY_PREFIX = 'https://fonts.google.com/download?family='


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

def get_repo_name(name):
    """Converts a ttf font path or font name into a gf repo font folder"""
    if name.endswith('.ttf'):
        name = name[:-4].split('-')[0]
    return basename(name.lower().replace(' ', ''))


def family_exists(name):
    """Check if a font family exists in the collection"""
    url_prefix = 'http://fonts.google.com/specimen/'
    dl_name = name.replace(' ', '+')
    url = url_prefix + dl_name
    request = requests.get(url)
    if request.status_code == 200:
        return True
    return False


def download_family_zip(name):
    """Downloads a family .zip file from fonts.google.com"""
    if family_exists(name):
        dl_url = DOWNLOAD_FAMILY_PREFIX + name.replace(' ', '+')
        family_zip = utils.download_file(dl_url)
        return ZipFile(family_zip)
    return None



if __name__ == '__main__':
    
    d = download_family_zip('Open Sans')
    print d.namelist()