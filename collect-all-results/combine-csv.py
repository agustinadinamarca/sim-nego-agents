import pandas as pd

all_filenames = ["results-srv-103.csv", "results-srv-104.csv", "results-srv-106.csv"]

#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
#export to csv
combined_csv.to_csv("results.csv", index=False, encoding='utf-8-sig')
