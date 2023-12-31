import requests
import pandas as pd

BASE_URL = "https://api.census.gov/data/"
# Zip code, median estimate household income, population of bachelor's degree and higher
VARIABLES = "NAME,S1903_C03_001E,S1501_C01_015E"
GEOGRAPHY = "&for=zip%20code%20tabulation%20area:"
ZIP_CODES = [78660, 78613, 78641, 78745, 78664, 78753, 78758, 78704, 78748, 78744, 78741, 78759, 78610, 78653, 78723, 78749, 78750, 78617, 78757, 78746, 78727, 78737, 78724, 78728, 78754, 78731, 78702, 78705, 78738, 78621, 78703, 78734, 78747, 78739, 78732, 78752, 78735, 78654, 78751, 78726, 78645, 78669, 78733, 78701, 78736, 78721, 78756, 78730, 78652, 78712, 78725, 78722, 78719, 78615, 78742, 78788, 78786, 78769, 78781, 78780, 78785, 78789, 78755, 73301, 73344, 78760, 78762, 78761, 78764, 78763, 78766, 78765, 78768, 78767, 78772, 78774, 78773, 78779, 78778, 78783, 78799, 78691, 78708, 78710, 78709, 78711, 78714, 78713, 78716, 78715, 78718, 78720]
ZIP_STR = ",".join(str(z) for z in ZIP_CODES)
CSV_FILE_PATH = 'data/demographic_data.csv'



# https://api.census.gov/data/{year}/acs/acs5/subject/groups/S1501.html
# https://api.census.gov/data/{year}/acs/acs5/subject/groups/S1903.html
YEAR_TO_COLUMNS = {
    2011: "S1903_C02_001E,S1501_C01_005E", # Median Income, % Bachelor's+
    2012: "S1903_C02_001E,S1501_C01_005E",
    2013: "S1903_C02_001E,S1501_C01_012E", # Median Income, % Bachelor's+ (25yo+)
    2014: "S1903_C02_001E,S1501_C01_012E", 
    2015: "S1903_C02_001E,S1501_C02_015E",
    2016: "S1903_C02_001E,S1501_C02_015E",
    2017: "S1903_C03_001E,S1501_C02_015E",
    2018: "S1903_C03_001E,S1501_C02_015E", # Median Income, % Bachelor's+ (25yo+)
    2019: "S1903_C03_001E,S1501_C02_015E",
    2020: "S1903_C03_001E,S1501_C02_015E",
    2021: "S1903_C03_001E,S1501_C02_015E"
}



def request_raw_data(year):
    """
    Requests Texas census data for a specific year from Census.gov.
    """
    params = f"NAME,{YEAR_TO_COLUMNS[year]}"
    in_state = "&in=state:48"
    if year < 2019:
        url = f"{BASE_URL}{year}/acs/acs5/subject?get={params}{in_state}{GEOGRAPHY}{ZIP_STR}"
    else:
        url = f"{BASE_URL}{year}/acs/acs5/subject?get={params}{GEOGRAPHY}{ZIP_STR}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad HTTP responses
        print(f"Retrieved data for {year}")
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f"Error occurred for year {year}: {err}")
        return None

# years = range(2011, 2022)
years = range(2011, 2022)
all_data = {}

for year in years:
    all_data[year] = request_raw_data(year)


def raw_into_df(all_data):
    """
    Transforms raw census data for multiple years into a combined dataframe.
    """
    combined_df = pd.DataFrame()

    for year, data in all_data.items():
        if data:
            if year < 2019:
                data[0][1:] = ["Median_Household_Income","Percent_Bachelors_Higher","State","Zip_Code"]
            else:
                data[0][1:] = ["Median_Household_Income","Percent_Bachelors_Higher","Zip_Code"]
            year_df = pd.DataFrame(data[1:], columns=data[0])
            year_df.drop("NAME", axis=1, inplace=True)
            if year < 2019:
                year_df.drop("State", axis=1, inplace=True)
            year_df["Zip_Code_Year"] = year_df["Zip_Code"].astype(str) + "_" + str(year)
            columns = ["Zip_Code_Year"] + [col for col in year_df.columns if col != "Zip_Code_Year"]
            year_df = year_df[columns]
            combined_df = pd.concat([combined_df, year_df], ignore_index=True)
            print(f"Added df for {year}")

    return combined_df

census_df = raw_into_df(all_data)

columns_to_convert = ["Median_Household_Income", "Percent_Bachelors_Higher"]
census_df[columns_to_convert] = census_df[columns_to_convert].astype(float)

census_df.to_csv(CSV_FILE_PATH, index=False)