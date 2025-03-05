import pandas as pd

df = pd.read_excel('assignment3/sources/scoring_data_v.1.2.xlsx', sheet_name='A2', header=None)

df.loc[1:50001, 0].to_csv('assignment3/sources/hashes.txt', index=False, header=False)
df.loc[1:5, 2].to_csv('assignment3/sources/phones.txt', index=False, header=False)