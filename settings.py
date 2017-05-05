import os

gf_api_url = 'http://tinyurl.com/m8o9k39'

production_fonts_dir = os.path.join(
    os.path.dirname(__file__),
    'out',
    'production_fonts'
)

production_fonts_renamed_dir = os.path.join(
    os.path.dirname(__file__),
    'out',
    'production_fonts_renamed'
)

production_fonts_fixed_dir = os.path.join(
    os.path.dirname(__file__),
    'out',
    'production_fonts_fixed'
)

description_dir = os.path.join('src', 'descriptions')

repo_url = 'https://github.com/google/fonts.git'
repo_cp_path = os.path.join('.', 'out', 'repo_cp')
