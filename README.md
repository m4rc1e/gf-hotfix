# GF collection wide hotfix 2017

Report/Update fonts which fail the following tests:
- OS/2 fsType
- OS/2 fsSelection
- OS/2 usWeightClass
- head macStyle
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