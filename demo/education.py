import pandas as pd

file_path = 'demo_data/ACSST5Y2011.S1501-2023-11-30T151241.csv'
data = pd.read_csv(file_path)

data_cleaned = data[~data['Label (Grouping)'].str.contains('Margin of Error', na=False)]

data_cleaned.loc[data_cleaned['Label (Grouping)'].str.contains('ZCTA5'), 'Label (Grouping)'] = \
    data_cleaned.loc[data_cleaned['Label (Grouping)'].str.contains('ZCTA5'), 'Label (Grouping)'].apply(lambda x: x.split()[1] + '_2011')

columns_to_remove = ["Less than high school graduate", "High school graduate (includes equivalency)", 
                     "Some college or associate's degree"]
data_cleaned.drop(columns=columns_to_remove, inplace=True)

output_file_path = 'demo_data/education_data_2011.csv'
data_cleaned.to_csv(output_file_path, index=False)

output_file_path
