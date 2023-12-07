import pandas as pd
from database import engine
from sqlalchemy import text

demo_data = pd.read_csv("data/demographic_data.csv", header=None, skiprows=1)
demo_data.to_csv("data/demographic_data_no_header.csv", index=False, header=False)
# print(demo_data.head())

create_extension = text("CREATE EXTENSION IF NOT EXISTS postgis")

with engine.connect() as connection:
    connection.execute(create_extension)


create_table_sql = text("""
    CREATE TABLE demographics (
        zip_code_year SERIAL PRIMARY KEY,
        median_household_income FLOAT,
        percent_bachelors_higher FLOAT,
        zip_code VARCHAR(10)
    )
""")

with engine.connect() as connection:
    connection.execute(create_table_sql)
