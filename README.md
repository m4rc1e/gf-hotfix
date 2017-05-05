# GF collection wide hotfix 2017

Hot fix the production fonts hosted on http://fonts.google.com.

The hotfix runs through the following sequence:
- Download the production fonts
- Rename the production fonts
- Generate report for renamed production fonts
- Fix the production fonts
- Generate report for fixed production fonts
- Make a copy of the google/fonts repo
- replace the old fonts with the fixed fonts, updated METADATA.pb and DESCRIPTION.en_us.html to the copied repo
- Push the updated families (manually done in chunks, too risky to gattling gun)


## Fixes which are applied to fonts
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

## Running the sequence
```
sh fix_fonts.sh
```