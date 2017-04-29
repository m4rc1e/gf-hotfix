# GF collection wide hotfix 2017


## Collection wide rounds:
R01: Fonts which already exist in google/fonts
R02: Fonts which do not have canonical names
R03: Fonts which need to be added to fonts.google.com
R04: Fonts which need to be added to google/fonts


## Fixes to be applied to fonts
- OS/2 fsType bit
- OS/2 fsSelection bit
- OS/2 usWeightClass bit
- head macStyle bit
- Name table


## Installation
```
git clone https://github.com/m4rc1e/gf-hotfix
cd gf-hotfix
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

## Generating reports
```
python generate_reports.py
```