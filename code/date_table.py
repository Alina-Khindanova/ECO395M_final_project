import pandas as pd
from database import engine
from sqlalchemy import text
from database import engine

#CODE TRANSACTION TO CREATE TABLE
create_dates_table = """
    CREATE TABLE IF NOT EXISTS date (
        "Date" DATE PRIMARY KEY,
        "Year" INT4,
        "Month" INT2
    );
"""

#CODE TRANSACTION TO PULL DATES FROM BUCKET
query_dates_data = """
SELECT 
    "Ocurred.Date" AS "Date"
FROM
    crime_reports
WHERE
    "Ocurred.Date" BETWEEN '2011-01-01' AND '2022-12-31';
"""

#CONNECT TO SQL SERVER WHERE I WILL PUSH THE DATA
engine.connect().exec_driver_sql(create_dates_table)

#RUN SQL QUERY
df_crime_dates = pd.read_sql_query(query_dates_data, engine)

#CODE YEAR AND MONTH COLUMNS
df_crime_dates_distinct= df_crime_dates.assign(Month = lambda x: x.Date.apply(lambda x: x.month), Year = lambda x: x.Date.apply(lambda x: x.year)).drop_duplicates()

#VERIFY ALL MONTHS AND YEARS ARE IN EACH COLUMN
print(df_crime_dates_distinct.Month.drop_duplicates().sort_values())
print(df_crime_dates_distinct.Year.drop_duplicates().sort_values())

#COMPARE NUMBER OF ROWS BETWEEN THE PREVIOUS TWO TABLES
print(f'sql query has {df_crime_dates.shape[0]} rows, but we have {df_crime_dates_distinct.shape[0]} unique dates (rows)')


#PUSH TABLE TO SQL SERVER 
df_crime_dates_distinct.to_sql("crime_dates", engine, if_exists="append", index=False)

#VERIFY THE TABLE IS IN THE CLOUD
#CODE TRANSACTION TO PULL DATES FROM BUCKET

# query_crime_dates_data = """
# SELECT 
#     *
# FROM
#     crime_dates
# """

# pd.read_sql_query(query_crime_dates_data, engine)
