from settings import (
    production_fonts_fixed_dir,
    production_fonts_renamed_dir
)
from report import check_fonts

check_fonts(production_fonts_renamed_dir, 'current')
check_fonts(production_fonts_fixed_dir, 'fixed')
