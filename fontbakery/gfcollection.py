from ntpath import basename
from datetime import datetime

from utils import api_request


gf_api_url = 'http://tinyurl.com/m8o9k39'


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

    def _parse_date(self, date):
        """Parse string date YYYY-MM-DD into datetime object"""
        date_parsed = tuple(map(int, date.split('-')))
        return datetime(*date_parsed)

    @property
    def family_count(self):
        return len([f for f in self.api_data['items']])


if __name__ == '__main__':
    from pprint import pprint
    c = ProductionServer()
    prd_families_in_production = [f['family'] for f in c.modified_after('2017-03-01')]
    print prd_families_in_production, len(prd_families_in_production)
    print c.family_count
