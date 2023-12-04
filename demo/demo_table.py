import pandas as pd
from database import engine
from sqlalchemy import text

demo_data = pd.read_csv("demo/demographic_data_no_header.csv", header=None)

print(demo_data.head())

create_extension = text("CREATE EXTENSION IF NOT EXISTS postgis")

with engine.connect() as connection:
    connection.execute(create_extension)

create_table_sql = text("""
    CREATE TABLE demographics (
        zipcode_year SERIAL PRIMARY KEY,
        median_household_income FLOAT,
        percent_bachelors_higher FLOAT,
        zip_code INTEGER
    )
""")

with engine.connect() as connection:
    connection.execute(create_table_sql)
