"""
Check how many outstanding prs have not made it into production yet
"""
import pandas as pd
import sys

from fontbakery.gfcollection import Repository, ProductionServer
from settings import sprint1_start


def main(username, password):
    repo = Repository(username, password)
    prs_merged = repo.families_merged_after(sprint1_start)
    prs_open = repo.families_unmerged_after(sprint1_start)

    gf_server = ProductionServer()
    families_in_production = [f['family'] for f in 
                              gf_server.modified_after(sprint1_start)]

    prs_merged = pd.Series(sorted(prs_merged))
    prs_open = pd.Series(sorted(prs_open))
    families_in_production = pd.Series(sorted(families_in_production))


    df = pd.concat([prs_open, prs_merged, families_in_production], axis=1)
    df.columns = ['Prs Open', 'Prs Merged', 'In Production']
    df.to_csv('./reports/hotfix_progress.csv',
              sep='\t', encoding='utf-8', index=False)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Please include your github username and password'
    else:
        main(sys.argv[1], sys.argv[2])
