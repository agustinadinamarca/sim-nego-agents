import os
import pandas as pd

all_filenames_r = ["partial-res-srv-103.csv", "partial-res-srv-104.csv", "partial-res-srv-106.csv"]

print('Obtaining partial-results.csv file...')
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames_r if os.path.exists(f)])
combined_csv = combined_csv.sort_values('id', ascending=True)
combined_csv.to_csv("partial-results.csv", index=False, encoding='utf-8-sig')
print('Done.')
