import pandas as pd
from database import engine
from sqlalchemy import text

drop_table = """
DROP TABLE IF EXISTS date
"""
#CODE TRANSACTION TO CREATE TABLE
create_date_table = """
    CREATE TABLE IF NOT EXISTS date (
        "Date" DATE PRIMARY KEY,
        "Year" INT4,
        "Month" INT2
    );
"""

#CODE TRANSACTION TO PULL DATES FROM BUCKET
query_date_data = """
SELECT 
    "Ocurred.Date" AS "Date"
FROM
    crime_reports
WHERE
    "Ocurred.Date" BETWEEN '2011-01-01' AND '2022-12-31';
"""

#CONNECT TO SQL SERVER WHERE I WILL PUSH THE DATA
engine.connect().exec_driver_sql(create_date_table)

#RUN SQL QUERY
df_crime_date = pd.read_sql_query(query_date_data, engine)

#CODE YEAR AND MONTH COLUMNS
df_crime_date_distinct= df_crime_date.assign(Month = lambda x: x.Date.apply(lambda x: x.month), Year = lambda x: x.Date.apply(lambda x: x.year)).drop_duplicates()

# #VERIFY ALL MONTHS AND YEARS ARE IN EACH COLUMN
# print(df_crime_date_distinct.Month.drop_duplicates().sort_values())
# print(df_crime_date_distinct.Year.drop_duplicates().sort_values())

# #COMPARE NUMBER OF ROWS BETWEEN THE PREVIOUS TWO TABLES
# print(f'sql query has {df_crime_date.shape[0]} rows, but we have {df_crime_date_distinct.shape[0]} unique date (rows)')


# #PUSH TABLE TO SQL SERVER 
df_crime_date_distinct.to_sql("date", engine, if_exists="append", index=False)

# #VERIFY THE TABLE IS IN THE CLOUD
# #CODE TRANSACTION TO PULL DATES FROM BUCKET

query_crime_date_data = """
SELECT 
    *
FROM
    crime_dates
"""

# pd.read_sql_query(query_crime_date_data, engine)
