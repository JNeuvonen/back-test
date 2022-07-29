import pandas as pd

file = pd.read_csv('combined-dataset.csv')

new_df = pd.concat([file['TSLA_OPEN'], file['TSLA_PREV_OPEN']], axis=1)

new_df.to_csv('inspect-data.csv')
