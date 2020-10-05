import pandas as pd
import numpy as np
from datetime import timedelta

# Loads NIRS data
def LoadCSV(filename, discard_by_status=False):
    df = pd.read_csv(filename,
                     sep = ',',
                     skiprows = 5,
                     na_values = ['--', ' '],
                     parse_dates = ['Time'])

    df.rename(columns={'rSO2 (%)': 'rSO2'}, inplace=True)
    df.rename(columns={'Poor Signal Quality': 'Bad_rSO2_auto'}, inplace=True)

    with open (filename, "r") as fd:
        next(fd)
        startdate = next(fd).partition(',')[2].strip()
        for _ in range(4): next(fd)
        startdate = startdate + 'T' + next(fd).partition(',')[0].strip()

    timeindex = []
    time = pd.to_datetime(startdate)
    for _ in range(len(df.index)):
        timeindex.append(time)
        time = time + timedelta(seconds=1)

    df['Time'] = timeindex
    df.set_index('Time', inplace=True)

    if discard_by_status == True:
        df['rSO2'] = np.where(df['Bad_rSO2_auto'] == 1, np.nan, df['rSO2'])

    #if amendments is not None:
    #    amend_df = pd.read_csv(amendments,
    #                           sep = ';',
    #                           na_values = ['--'],
    #                           parse_dates = ['Time'])

    #    amend_df = amend_df.replace({'Mark': ' '}, '0')
    #    df['Mark'] = amend_df['Mark'].array
    #    df['Bad_rSO2_manual'] = amend_df['HuonoSignaali2'].array

    return df
