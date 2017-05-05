import os
from settings import (
    production_fonts_renamed_dir
)
from report import check_fonts

if not os.path.isdir('reports'):
    os.mkdir('reports')

check_fonts(production_fonts_renamed_dir, 'current')
