import re
import gfspec


NON_UNICASE_NAMES = {
    'IMFELLGreatPrimer': 'IM FELL Great Primer',
    'BiryaniUltraLight': 'Biryani UltraLight',
    'CantoraOne': 'CantoraOne',
    'IMFELLDoublePicaSC': 'IM FELL Double Pica SC',
    'IMFELLGreatPrimerSC': 'IM FELL Great Primer SC',
    'UnifrakturMaguntia': 'UnifrakturMaguntia',
    'PlayfairDisplaySC': 'Playfair Display SC',
    'PTSerifCaption': 'PT Serif Caption',
    'NTR': 'NTR',
    'MontserratAlternatesExLight': 'Montserrat Alternates ExLight',
    'DiplomataSC': 'Diplomata SC',
    'McLaren': 'McLaren',
    'OdorMeanChey': 'OdorMeanChey',
    'PTSans': 'PT Sans',
    'VT323': 'VT323',
    'GFSDidot': 'GFS Didot',
    'IMFELLFrenchCanon': 'IM FELL French Canon',
    'PressStart2P': 'Press Start 2P',
    'BenchNine': 'BenchNine',
    'MartelUltraLight': 'Martel UltraLight',
    'BioRhyme': 'BioRhyme',
    'MateSC': 'Mate SC',
    'SirinStencil': 'SirinStencil',
    'CormorantSC': 'Cormorant SC',
    'IMFELLEnglish': 'IM FELL English',
    'IMFELLDWPicaSC': 'IM FELL DW Pica SC',
    'HammersmithOne': 'HammersmithOne',
    'OldStandardTT': 'Old Standard TT',
    'NovaMono': 'NovaMono',
    'AmaticSC': 'Amatic SC',
    'AlmendraSC': 'Almendra SC',
    'BioRhymeExpanded': 'BioRhyme Expanded',
    'BiryaniDemiBold': 'Biryani DemiBold',
    'IMFELLDoublePica': 'IM FELL Double Pica',
    'PTSansCaption': 'PT Sans Caption',
    'MartelDemiBold': 'Martel DemiBold',
    'IMFELLEnglishSC': 'IM FELL English SC',
    'HoltwoodOneSC': 'Holtwood One SC',
    'EBGaramond': 'EB Garamond',
    'CarroisGothicSC': 'Carrois Gothic SC',
    'GFSNeohellenic': 'GFS Neohellenic',
    'PTSansNarrow': 'PT Sans Narrow',
    'MarcellusSC': 'Marcellus SC',
    'IMFELLDWPica': 'IM FELL DW Pica',
    'AmaticaSC': 'Amatica SC',
    'OverlockSC': 'Overlock SC',
    'MedievalSharp': 'MedievalSharp',
    'PTSerif': 'PT Serif',
    'IMFELLFrenchCanonSC': 'IM FELL French Canon SC',
    'UnifrakturCook': 'UnifrakturCook',
    'PatrickHandSC': 'Patrick Hand SC',
    'PTMono': 'PT Mono',
    'HeadlandOne': 'HeadlandOne',
    'ABeeZee': 'ABeeZee',
    'BowlbyOneSC': 'Bowlby One SC',
    'AlegreyaSansSC': 'Alegreya Sans SC',
    'AlegreyaSC': 'Alegreya SC',
    'Exo2': 'Exo 2',
    'MountainsofChristmas': 'Mountains of Christmas',
    'NunitoSansVFBeta', 'Nunito Sans VF Beta',
    'RalewayVFBeta', 'Raleway VF Beta',
    'RokkittVFBeta', 'Rokkitt VF Beta',
    'ManualeVFBeta', 'Manuale VF Beta',
    'MavenProVFBeta', 'Maven Pro VF Beta',
    'OswaldVFBeta', 'Oswald VF Beta',
    'NunitoVFBeta', 'Nunito VF Beta',
    'YanoneKaffeesatzVFBeta', 'Yanone Kaffeesatz VF Beta',
    'UnnaVFBeta', 'Unna VF Beta',
    'EncodeSansVFBeta', 'Encode Sans VF Beta',
    'OverpassVFBeta', 'Overpass VF Beta',
    'DosisVFBeta', 'Dosis VF Beta',
    'ArchivoVFBeta', 'Archivo VF Beta',
    'CabinVFBeta', 'Cabin VF Beta',
    'FaustinaVFBeta', 'Faustina VF Beta',
    'SansitaVFBeta', 'Sansita VF Beta',
    'AsapVFBeta', 'Asap VF Beta',
    'PodkovaVFBeta', 'Podkova VF Beta',
}

def get_familyname(ttfont):
    """Get the name of a font file"""
    name = ttfont['name'].getName(1, 3, 1, 1033).string.decode('utf_16_be')
    for style in gfspec.STYLES:
        if style in name:
            name = name.replace(' '+style, '')
    return name


def get_repo_name(name):
    """Converts a ttf font path or font name into a gf repo font folder"""
    if name.endswith('.ttf'):
        name = name[:-4].split('-')[0]
    return basename(name.lower().replace(' ', ''))


def familyname_from_filename(filename):
    """Derive the family name from a filename
    OpenSans-Regular.ttf -> Open Sans.

    Warning: This method is not 100% accurate. Some filenames do not match
    their font menu names, PT_Sans_Web etc."""
    family_name = filename.split('-')[0]
    family_name = family_name.replace('.ttf', '')
    if family_name in NON_UNICASE_NAMES:
        return NON_UNICASE_NAMES[family_name]
    # RubikMonoOne -> Rubik Mono One
    return re.sub('(?!^)([A-Z]|[0-9]+)', r'%s\1' % ' ', family_name)


def get_version(ttfont):
    """Return the font version from the head table to 3 decimal places"""
    return '%.3f' % ttfont['head'].fontRevision


def is_canonical(filename):
    if '-' in filename:
        return True
    return False


def increment_version_number(ttfont, inc):
    """Increment a fonts version number.

    Update the name records and head.fontRevision. If a versions name records
    is badly formatted, create a new one from the head.fontRevision."""
    version_pattern = r'[0-9]{1,4}\.[0-9]{1,4}'
    name_table = ttfont['name']
    for name in name_table.names:

        if name.nameID in [3, 5]:
            enc = 'mac-roman' if name.langID == 0 else 'utf_16_be'
            record_text = name.string

            version = re.search(version_pattern, record_text)

            if version:
                current_version = float(version.group())
                new_version = float(version.group()) + inc

                new_record_text = record_text.replace(
                    "%.3f" % current_version,
                    "%.3f" % new_version
                )
            else:
                new_version = float(ttfont['head'].fontRevision) + inc
                new_record_text = 'Version %.3f' % new_version

            name_table.setName(
                new_record_text.encode(enc),
                name.nameID,
                name.platformID,
                name.platEncID,
                name.langID,
            )

            ttfont['head'].fontRevision = new_version
