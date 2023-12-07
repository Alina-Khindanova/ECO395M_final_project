import pandas as pd

"""
Zip codes included in data:

ZIP_CODES_INCLUDED = [78610,78613,78615,78617,78621,78641,78645,78652,78653,78654,78660,78664,78669,78701,78702,78703,78704,78705,78712,78719,78721,78722,78723,78724,78725,78726,78727,78728,78730,78731,78732,78733,78734,78735,78736,78737,78738,78739,78741,78742,78744,78745,78746,78747,78748,78749,78750,78751,78752,78753,78754,78756,78757,78758,78759]


Zip codes missing in data:

ZIP_CODES_EXCLUDED = [78788, 78786, 78769, 78781, 78780, 78785, 78789, 78755, 73301, 73344, 78760, 78762, 78761, 78764, 78763, 78766, 78765, 78768, 78767, 78772, 78774, 78773, 78779, 78778, 78783, 78799, 78691, 78708, 78710, 78709, 78711, 78714, 78713, 78716, 78715, 78718, 78720]
"""

ZIP_CODES = [78660, 78613, 78641, 78745, 78664, 78753, 78758, 78704, 78748, 78744, 78741, 78759, 78610, 78653, 78723, 78749, 78750, 78617, 78757, 78746, 78727, 78737, 78724, 78728, 78754, 78731, 78702, 78705, 78738, 78621, 78703, 78734, 78747, 78739, 78732, 78752, 78735, 78654, 78751, 78726, 78645, 78669, 78733, 78701, 78736, 78721, 78756, 78730, 78652, 78712, 78725, 78722, 78719, 78615, 78742, 78788, 78786, 78769, 78781, 78780, 78785, 78789, 78755, 73301, 73344, 78760, 78762, 78761, 78764, 78763, 78766, 78765, 78768, 78767, 78772, 78774, 78773, 78779, 78778, 78783, 78799, 78691, 78708, 78710, 78709, 78711, 78714, 78713, 78716, 78715, 78718, 78720]

df = pd.read_csv("data/demographic_data.csv")

# Add a "Year" column
df["Year"] = df["Zip_Code_Year"].apply(lambda x: x.split("_")[1])

# Check missing zip codes
years_range = [str(year) for year in range(2011, 2022)]
missing_zip_codes_by_year = {}

for year in years_range:
    zip_codes_this_year = set(df[df["Year"] == year]["Zip_Code"])
    missing_zip_codes = [zip_code for zip_code in ZIP_CODES if zip_code not in zip_codes_this_year]
    missing_zip_codes_by_year[year] = missing_zip_codes

# Printing missing ZIP codes by year
for year, missing_zip_codes in missing_zip_codes_by_year.items():
    print(f"Missing ZIP codes in {year}: {missing_zip_codes}")

df.to_csv("data/demographic_data_modified.csv", index=False)

