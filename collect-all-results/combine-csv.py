import os
import pandas as pd



all_filenames = ["results-srv-103.csv", "results-srv-104.csv", "results-srv-106.csv"]

print('Obtaining results.csv file...')
combined_csv = pd.concat([pd.read_csv(f, sep=',') for f in all_filenames if os.path.exists(f)])
combined_csv = combined_csv.sort_values(by='id', ascending=True)
combined_csv.to_csv("results.csv", index=False, encoding='utf-8-sig')
print('Done.')
