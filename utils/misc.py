import pandas as pd
import datetime

# make timestamp column 'Time' start from Unix epoch 1.1.1970 00:00
def NormalizeTimeIndex(df):
    epoch = datetime.datetime.utcfromtimestamp(0)
    diff = df.index[0] - epoch
    df.index -= diff

# remove rows containing no MAP or NIRS data
def TrimData(df):
    mark_timestamp = df.loc[df['Mark'] == 1].index[0]
    start = min(df['rSO2'].first_valid_index(),
                df['MAP'].first_valid_index(),
                mark_timestamp)
    end = max(df['rSO2'].last_valid_index(), df['MAP'].last_valid_index())
    timerange = pd.date_range(start=start, end=end, freq='s')
    return df.reindex(timerange).rename_axis('Time')

# Delay MAP signal and its data elimination markers Bad_MAP_auto &
# Bad_MAP_manual by t seconds. Resize dataframe to fit all values.
def ShiftMAP(df, t):
    if (t == 0): return df
    mark_timestamp = df.loc[df['Mark'] == 1].index[0]
    first_map = df['MAP'].first_valid_index()
    last_map = df['MAP'].last_valid_index()
    delta = pd.Timedelta(seconds=abs(t))
    if (t < 0):
        first_map -= delta
        last_map -= delta
    elif (t > 0):
        first_map += delta
        last_map += delta
    start = min(df['rSO2'].first_valid_index(), first_map, mark_timestamp)
    end = max(df['rSO2'].last_valid_index(), last_map)
    timerange = pd.date_range(start=start, end=end, freq='s')
    df = df.reindex(timerange).rename_axis('Time')
    df['MAP'] = df['MAP'].shift(t)
    df['Bad_MAP_auto'] = df['Bad_MAP_auto'].shift(t).fillna(0).astype(int)
    df['Bad_MAP_manual'] = df['Bad_MAP_manual'].shift(t).fillna(0).astype(int)
    df['Bad_rSO2_auto'] = df['Bad_rSO2_auto'].fillna(0).astype(int)
    df['Bad_rSO2_manual'] = df['Bad_rSO2_manual'].fillna(0).astype(int)
    df['Mark'] = df['Mark'].fillna(0).astype(int)
    NormalizeTimeIndex(df)
    return df

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