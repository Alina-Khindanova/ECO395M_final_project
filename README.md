# Crime over time:

## Examining Changes in Crimes Reported in the Greater Austin Area over the Last Twelve Years

December 7, 2023

Alina Khindanova, Audrey Peres, Lydia Liu, & Marco Rodriguez

# Introduction 

In this project, we analyze the changes in the number of crimes happened in the Greater Austin Area between 2011 and 2022. In particular, we look at the distribution of the number of crimes across geographical areas and analyze distinctions in distributions between different types of crime over the years. We construct an interactive dashboard in Streamlit displaying the count of crimes across various zip code areas, categorized by crime type and year. Additionally, to potentially elucidate insights, we generate scatterplots illustrating the relationship between crime numbers and demographic characteristics. Our data on crime reports come from the City of Austin Open Data Portal and demographics information is obtained from U.S. Census Bureau’s American Community Survey (ACS). Although there was a decrease in the number of reported incidents across all crime categories, the geographical distribution of these crimes did not exhibit significant changes.

# Data

1. Crime Report Data

Crime reports file from the [City of Austin Open Data Portal](https://data.austintexas.gov/Public-Safety/Crime-Reports/fdj4-gpfu/about_data). This dataset contains a record of incidents to which the Austin Police Department responded and subsequently filed a report. The following variables are used for the analysis:

- Highest offense description (a name of the most severe offense associated with an incident)
- Highest offense code (3- or 4-digit number corresponding to the description)
- Occurred Date
- Zip Code (where an incident occurred)

2. Demographic Data

Demographic Data is from the [U.S. Census Bureau’s American Community Survey (ACS)](https://www.census.gov/data/developers/data-sets/acs-1year.html). Among the variety of demographic characteristics presented in the data, we decided to concentrate on income and education as we expect these factors to correlate most with the crime numbers. The data includes the zip codes for Travis County, the median household income for each zip code from 2011 to 2021, and the percent of the population of the zip code area 18 years or older with a bachelor's degree or higher from 2011 to 2021. The variables are labeled:

- Median_Household_Income
- Percent_Bachelors_Higher
- Zip_Code
- Year

3. Geographic data

The U.S. Census Bureau provided geographic data, which was obtained in the form of zip files containing cartographic boundary shape files. These files delineate boundaries for each [Zip Code](https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.2020.html#list-tab-1883739534) and [census tract](https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.2022.html#list-tab-1883739534) in Texas and are crucial for incorporating an interactive map into the dashboard.



# Running the Code




# Methodology

1. Data Collection

2. Database Creation

3. Creating Streamlit App


# Results


# Limitations and Extensions

1. Data



2. Methodology



# Conclusion


