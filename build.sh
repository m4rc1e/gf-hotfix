#!/bin/bash

set -e # Stop script if we have any critical errors

python download_production_fonts.py
python rename_production_fonts.py
python generate_reports_before_fix.py
python fix_renamed_production_fonts.py
python generate_reports_after_fix.py
python rebuild_repo_tree.py
echo 'Repository rebuilt with fixed fonts ./out/repo_cp'
