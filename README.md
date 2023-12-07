# Crime over time:

## Examining Changes in Crimes Reported in the Greater Austin Area over the Last Twelve Years

December 7, 2023

Alina Khindanova, Audrey Peres, Lydia Liu, & Marco Rodriguez

# Introduction 

In this project, we analyze the changes in the number of crimes happened in the Greater Austin Area between 2011 and 2022. In particular, we look at the distribution of the number of crimes across geographical areas and analyze distinctions in distributions between different types of crime over the years. We construct an interactive dashboard in Streamlit displaying the count of crimes across various zip code areas, categorized by crime type and year. Additionally, to potentially elucidate insights, we generate scatterplots illustrating the relationship between crime numbers and demographic characteristics. Our data on crime reports come from the City of Austin Open Data Portal and demographics information is obtained from U.S. Census Bureau’s American Community Survey (ACS). Although there was a decrease in the number of reported incidents across all crime categories, the geographical distribution of these crimes did not exhibit significant changes.

# Data

**1. Crime Report Data**

Crime reports file from the [City of Austin Open Data Portal](https://data.austintexas.gov/Public-Safety/Crime-Reports/fdj4-gpfu/about_data). This dataset contains a record of incidents to which the Austin Police Department responded and subsequently filed a report. The following variables are used for the analysis:

- Highest offense description (a name of the most severe offense associated with an incident)
- Highest offense code (3- or 4-digit number corresponding to the description)
- Occurred Date
- Zip Code (where an incident occurred)

**2. Demographic Data**

Demographic Data is from the [U.S. Census Bureau’s American Community Survey (ACS)](https://www.census.gov/data/developers/data-sets/acs-1year.html). Among the variety of demographic characteristics presented in the data, we decided to concentrate on income and education as we expect these factors to correlate most with the crime numbers. The data includes the zip codes for Travis County, the median household income for each zip code from 2011 to 2021, and the percent of the population of the zip code area 18 years or older with a bachelor's degree or higher from 2011 to 2021. The variables are labeled:

- Median_Household_Income
- Percent_Bachelors_Higher
- Zip_Code
- Year

**3. Geographic data**

The U.S. Census Bureau provided geographic data, which was obtained in the form of zip files containing cartographic boundary shape files. These files delineate boundaries for each [Zip Code](https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.2020.html#list-tab-1883739534) and [census tract](https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.2022.html#list-tab-1883739534) in Texas and are crucial for incorporating an interactive map into the dashboard.



# Running the Code




# Methodology

**1. Data Collection**

- Crime Report Data

    Crime reports CSV file is from the [City of Austin Open Data Portal](https://data.austintexas.gov/Public-Safety/Crime-Reports/fdj4-gpfu) as mentioned before, the original data can be downloaded from the website directly, which contains 2.4 million records from 2003 to 2023. 

- Demographic Data

    Using an API key for the U.S. Census Bureau’s American Community Survey. After the data was retrieved, a new variable called “zip_code_year” was created, combining the zip code and year of each data point. Therefore, each data point of median household income and percentage of the population with a bachelor's degree or higher was unique for each year and zip code, tracking changes in a specific area over time. 

- Geographic Data

    The data was obtained from the U.S. Census Bureau's Cartographic Boundary Files page. To acquire [census tract data](https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.2022.html#list-tab-1883739534), scroll down to the census tract header, choose Texas in the shapefile select box, and download the 'cb_2022_48_tract_500k' zip file. Similarly, for [Zip Code data](https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.2020.html#list-tab-1883739534), scroll down to ZIP Code Tabulation Areas (ZCTAs), and download the 'cb_2020_us_zcta520_500k' shapefile. Store both files in the designated GCP bucket.


**2. Database Creation**

- Crime Reports Table

    This is the main table of the database, containing all the crime-related information to be included in the final dashboard. After creating the table, the downloaded file was stored in a GCP bucket without the headers and with the variables in the same order as the SQL table created. Finally, the table was filled manually in the GCP console with the mentioned CSV file.

- Crime Type Table

    Within the Crime Report Data, there exist 362 distinct crime types, each denoted by a unique Highest Offensive Description. The Highest Offensive Code serves as the corresponding numerical identifier for these descriptions. Utilizing ChatGPT, we systematically classified the 362 crime types into six primary categories: Violent Crimes, Property Crimes, White-collar Crimes, Drug-Related Crimes, Cybercrimes, and Others. Keyword analysis was used, and ChatGPT parsed keywords from the original categories and allocated them to the six overarching type. Specifically, we identified 31 keywords for Violent Crimes, 12 for Property Crimes, 18 for White-collar Crimes, 7 for Drug-Related Crimes, and 9 for Cybercrimes; any remaining keywords were allocated to the "Others" category. The resultant classifications were recorded in the "crime.type" column, yielding the following summary:

    - Other: 137
    - Violent Crimes: 112
    - Property Crimes: 48
    - White-collar Crimes: 27
    - Drug-Related Crimes: 26
    - Cybercrimes: 12.

    The crime type table contains three columns: Highest.Offensive.Code, serving as the primary key linked to other tables; Highest.Offensive.Description, offering a textual depiction of the corresponding code and crime.type, housing the newly assigned crime categories.

- Demographics Table

    Once this demographics csv file was created, it was uploaded to the Google Cloud database called “crime” and stored as a table called “demographics”. Using the unique zip code and year as the table's primary key, we could relate it to the information in the crime_reports table using the respective zip code and year available in that table. We used this information for the scatterplots we created in the Streamlit App.

- Zip Code and Census Tracts Tables

    These tables store pertinent geographic boundaries, with the original information contained in the above mentioned zip files. Following the data download, the zip files were uploaded to a GCP bucket. Subsequently, the tables were created and populated by connecting Python to the GCP database and bucket, utilizing the database credentials and the GCP key in JSON format.


**3. Creating Streamlit App**

Utilizing Python, SQL queries were employed to extract pertinent data from the generated database. Subsequently, the acquired data was used to generate descriptive summaries and plots, contributing to the characterization of crime geographic distribution, temporal evolution, and its correlation with specific demographic variables. The information produced is displayed within a Streamlit dashboard. Below is a brief description of the content.

- Descriptive summaries:

    The presentation included the average annual number of crime reports throughout the analyzed period, along with the proportional contribution of each crime type to the total.

- Temporal evolution:

    A monthly series graph for each type of crime was included to examine the evolution of crime reports throughout the period.

- Interactive map:

    An interactive map was incorporated to depict the geographical distribution of crime reports. The map utilizes Zip Code boundaries, enabling the selection of crime type and year to display the distribution for each type within the chosen timeframe.

- Demographics scatterplots:

    - Using the crime_reports and demographics tables, we created two scatterplots. 
    - The first scatterplot examines the correlation between the number of crimes reported in a certain zip code within a certain year and the median household income for that specific zip code within a specific year. 
    - The second scatterplot shows the correlation between the number of crimes in a certain zip code within a certain year and the population over 18 with a bachelor's degree or higher.


# Results

Combining the data for all 12 years, the average number of crime reports per year is 97,516, and the most common category of crime considered in the analysis was property-related crimes (46.4%). Then comes violent crimes (24.5%), drug-related crimes (9.4%), white-collar crimes (3.2%), and cybercrimes (0.3%).

The plot below shows the dynamics of the crime numbers for different types of crimes for years 2011-2023.This graph confirms the previous results of the dominating role of property crimes, with more than 3,000 incidents every month. Overall, the number of crimes decreased for all types of crimes. We can see a significant decline in the property crimes, as well as violent crimes, and also a more pronounced seasonality component in these two types of crimes. However, it is important to note that property crimes experienced a disruption in their downward trend during the pandemic.

![number_of_crime_reports](https://raw.githubusercontent.com/Alina-Khindanova/ECO395M_final_project/readme/artifacts/Number%20of%20crime%20reports%20per%20month%20(1).png)


# Limitations and Extensions

1. Data



2. Methodology



# Conclusion


