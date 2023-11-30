import pandas as pd         

file_path = "demo/demo_data/ACSST5Y2021.S1901-2023-11-30T151915.csv"
df = pd.read_csv(file_path)

df_filtered = df[~df["Label (Grouping)"].str.contains("Margin of Error")]

df_filtered["Label (Grouping)"] = df_filtered["Label (Grouping)"].apply(
    lambda x: x.strip() + "_2021" if "ZCTA5" in x else x
)

df_filtered["Label (Grouping)"] = df_filtered["Label (Grouping)"].str.replace("ZCTA5 ", "")

output_file_path = "demo/demo_data/income_data_2021.csv"
df_filtered.to_csv(output_file_path, index=False)