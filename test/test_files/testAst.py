import pandas as pd

df1 = pd.DataFrame({'lkey': ['foo', 'bar', 'baz', 'foo'],
                    'value': [1, 2, 3, 5]})
df2 = pd.DataFrame({'rkey': ['foo', 'bar', 'baz', 'foo'],
                    'value': [5, 6, 7, 8]})

for i in df1.itertuples():
    print(i)
print(df1)

merged_df = pd.merge(df1, df2, how='left')
print(merged_df)

df = pd.read_csv("data.csv", dtype={'a': 'Int64'}, usecols=['a'])