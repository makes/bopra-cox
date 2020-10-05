import datetime

# make timestamp column 'Time' start from Unix epoch 1.1.1970 00:00
def NormalizeTime(df):
    epoch = datetime.datetime.utcfromtimestamp(0)
    diff = df['Time'][0] - epoch
    df['Time'] -= diff

# add column containing elapsed time as a fraction of total duration
def CreateElapsedTimeColumn(df):
    t_start = df['Time'].iloc[0]
    t_end = df['Time'].iloc[-1]
    t_tot = t_end - t_start
    elapsed = []
    for _, row in df.iterrows():
        t = row['Time'] - t_start
        elapsed.append(t / t_tot)
    df['Elapsed'] = elapsed
    return t_start.to_pydatetime(), t_end.to_pydatetime()

def GetRanges(df, colname):
    ranges = []
    range_start = None
    for index, row in df.iterrows():
        if row[colname] == 1 and range_start is None:
            range_start = index
        if row[colname] == 0 and range_start is not None:
            ranges.append((range_start, index))
            range_start = None
    if range_start is not None:
        ranges.append((range_start, df.index[-1]))
    return ranges