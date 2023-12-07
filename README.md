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

Step 1: Our code will be executed in a Python environment and required packages can be installed with `pip install -r requirements.txt`

Step 2: Table Creation:

Prior to executing the Python code, download the 
    1. [crime_reports CSV file](https://data.austintexas.gov/Public-Safety/Crime-Reports/fdj4-gpfu/data_preview)
    2. [geographic data](https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.2022.html#list-tab-1883739534) (ZIP Code Tabulation Areas (ZCTAs) and Census Tracts) 

(See *Methodology → Data Collection→ Geographic data for more details*)
upload them to a GCP bucket due to its large size. Ensure that the crime reports file does not contain headers.

Before running the python code, you must give it the right credentials to connect to your database. Copy the file `demo.env` to `.env` and modify it by providing the credentials.

`database.py` in the code folder serves as an engine and connection between google cloud platform and Dbeaver. 

Running the code:
    1. Run `python code/geography_table.py`
    2. Load headless crime_reports CSV into the crime_reports table with the import option in GCP SQL instance's console.
    3. Then run the following commands:
        - `python code/crime_type_table.py`
        - `python code/date_table.py`
    These commands will create and export tables directly to DBeaver.
    4. For the demographic table:
        - Run `python code/demo.py` to script demographic data from the website. This data will be stored in data/demographic_data.csv.
        - Run `python code/demo_table.py` to create a SQL table and export the data to DBeaver.

Step3: Dashboard Creation using Streamlit 

To access the interactive dashboard for insights into Austin's crime data from 2011 to 2023, execute the command `streamlit run code/dashboard.py` This will enable you to interactively select and view crime data by changing the "Crime Type" and "Select Year" parameters for different results.




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

    The first step in our code is to add an extension to our PostgreSQL database to handle geographic data using POSTGIS. These tables store pertinent geographic boundaries, with the original information contained in the above mentioned zip files. Following the data download, the zip files were uploaded to a GCP bucket. Subsequently, the tables were created and populated by connecting Python to the GCP database and bucket, utilizing the database credentials and the GCP key in JSON format.


**3. Creating Streamlit App**

Utilizing Python, SQL queries were employed to extract pertinent data from the generated database. Subsequently, the acquired data was used to generate descriptive summaries and plots, contributing to the characterization of crime geographic distribution, temporal evolution, and its correlation with specific demographic variables. The information produced is displayed within a Streamlit dashboard. Below is a brief description of the content.

- Descriptive summaries:

    The presentation included the average annual number of crime reports throughout the analyzed period and the proportional contribution of each crime type to the total.

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

![number_of_crime_reports](https://raw.githubusercontent.com/Alina-Khindanova/ECO395M_final_project/main/artifacts/Number%20of%20crime%20reports%20per%20month.png)

Another piece of the dashboard, the interactive map, shows how the count of crimes changes across various zip code areas for different types of crime. The common trend for all categories is that most of the crimes are concentrated in the Austin city, and less crimes committed in the nearby areas. This could be connected with the fact that central areas are usually more crowded, and many more people live, work or commute here. The most dangerous areas for most of the categories are located in the northern (zip codes 78753, 78758) and eastern (78704, 78741) parts of Austin.

Below are the screens of the geographic distributions for the most common categories of crime - property crimes and violent crimes. We choose to show years 2011, 2016, and 2022 in order to show the beginning of the considered period, middle, and the end. It's evident from our analysis that the distributions of crimes have remained relatively stable throughout the studied period.

<img src="https://raw.githubusercontent.com/Alina-Khindanova/ECO395M_final_project/main/artifacts/property_crimes_per_zipcode/Property%20Crimes%20per%20Zipcode%20in%202011.png" width="250" height="2500"> <img src="https://raw.githubusercontent.com/Alina-Khindanova/ECO395M_final_project/main/artifacts/property_crimes_per_zipcode/Property%20Crimes%20per%20Zipcode%20in%202016.png" width="250" height="250"> <img src="https://raw.githubusercontent.com/Alina-Khindanova/ECO395M_final_project/main/artifacts/property_crimes_per_zipcode/Property%20Crimes%20per%20Zipcode%20in%202022.png" width="250" height="250">


<img src="https://raw.githubusercontent.com/Alina-Khindanova/ECO395M_final_project/main/artifacts/violent_crimes_per_zipcode/Violent%20Crimes%20per%20Zipcode%20in%202011.png" width="250" height="250"> <img src="https://raw.githubusercontent.com/Alina-Khindanova/ECO395M_final_project/main/artifacts/violent_crimes_per_zipcode/Violent%20Crimes%20per%20Zipcode%20in%202016.png" width="250" height="250"> <img src="https://raw.githubusercontent.com/Alina-Khindanova/ECO395M_final_project/main/artifacts/violent_crimes_per_zipcode/Violent%20Crimes%20per%20Zipcode%20in%202022.png" width="250" height="250">

We expanded our analysis illustrating correlations between demographic characteristics and number of crimes. We can see a negative correlation between crime reports counts and median household income. This suggests that individuals with lower incomes are more frequently involved or detected in these incidents. Additionally, our analysis reveals a negative correlation between the count of crime reports and the percentage of individuals aged 18 years or older holding a bachelor’s degree or higher. It could be the case that more educated people are less likely to be involved in an incident. However, to draw concrete conclusions regarding this correlation, it's crucial to investigate whether the majority of individuals involved in crimes reside in the same zip code areas where the incidents occurred.

![income_crime](https://raw.githubusercontent.com/Alina-Khindanova/ECO395M_final_project/main/artifacts/demographic_scatter_plot/Scatter%20Plot%20of%20Median%20Household%20Income%20vs%20Crime%20Reports%20Count.png) ![educ_crime](https://raw.githubusercontent.com/Alina-Khindanova/ECO395M_final_project/main/artifacts/demographic_scatter_plot/Scatter%20Plot%20of%20Percent%20with%20Bachelor's%20Degree%20or%20Higher%20vs%20Crime%20Reports%20Count.png)


# Limitations and Extensions

1. Data

Crime Reports table: 

It is important to keep in mind that the crime reports dataset contains records of incidents that the Austin Police Department responded to and wrote a report. In addition, one incident may have several offenses associated with it, but this dataset only depicts the highest level offense of that incident.

Crime Type table:
When we used ChatGPT to sort 362 different crime types into six main categories using keywords, there are some limitations because the original crime descriptions in the dataset are too general, making it challenging to neatly fit them into simple categories. The act of categorizing crimes is also debatable, as it depends a lot on specific situations. To improve accuracy, it would be wise to explore a more sophisticated model that can better handle the complexities and context of crime data.

Demographics table:
The data was only available from 2011-2021, so the amount of periods was limited. Also, the American Community Survey had missing data points for some zip codes in different years, so the results could change if more data points were available. In addition, a portion of the population ages 22-24 who have a bachelor's degree are absent in the data, due to the populations being divided as 18 to 24 years old and 25 and older.

Geographic data: 
We analyze crime data using Zip code boundaries as the relevant geographic division. This approach was not compared to an analysis using another type of geographic division that could potentially provide further insights into the geographic distribution of crime. A natural extension would be to include more granular geographic data.



2. Methodology

The primary outcome variable, the number of reported crimes, may exhibit a high correlation with the population count residing in a particular area. Utilizing a relative indicator could potentially mitigate this correlation. However, it's essential to consider the possibility of individuals commuting from their residences to commit crimes, which might distort the accuracy of a relative indicator's representation.

As was discussed in the results section, in order to draw better conclusions regarding the effect of demographic characteristics, we need to check whether the majority of people committed crimes in the zip code area where they are living.



# Conclusion

This project provides a descriptive analysis of the number of crimes happened in the Greater Austin Area in 2011-2022. The interactive dashboard shows any dynamic changes happened in every zip code for every category of crime. We found that the geographical distribution did not change a lot, but the number of crimes dropped. Demographics characteristics could potentially play a big role on the number of crimes, however, additional analysis is needed in order to identify a causal relationship.
