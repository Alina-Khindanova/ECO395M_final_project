import pandas as pd
import geopandas as gpd
import os
import json
from sqlalchemy import Column, Integer, String, DateTime
from geoalchemy2 import Geometry, WKTElement
from database import engine
from dotenv import load_dotenv
from google.cloud import storage
from google.oauth2 import service_account
from io import BytesIO
from io import StringIO

# LOAD CREDENTIALS
load_dotenv()

json_key_string = os.getenv("JSON_KEY_STRING")
json_gcp_key = json.loads(json_key_string, strict=False)
credentials = service_account.Credentials.from_service_account_info(
    json_gcp_key, scopes=["https://www.googleapis.com/auth/cloud-platform"]
)
client = storage.Client(credentials=credentials)
bucket_name = os.getenv("BUCKET_NAME")
bucket = client.bucket(bucket_name)


# CREATE TABLES
def run_query(query):
    engine.connect().exec_driver_sql(query)


create_extension = """
    CREATE EXTENSION IF NOT EXISTS postgis
"""

create_zipcode_table = """
    CREATE TABLE IF NOT EXISTS zipcode (
        id SERIAL PRIMARY KEY,
        "ZCTA5CE20" Numeric,
        "AFFGEOID20" VARCHAR,
        "GEOID20" VARCHAR,
        zip_code VARCHAR,
        "LSAD20" VARCHAR,
        "ALAND20" Numeric,
        "AWATER20" Numeric,
        geometry_wkt geometry(Geometry, 4326)
    );
"""

create_censustract_table = """
    CREATE TABLE IF NOT EXISTS census_tract (
        id SERIAL PRIMARY KEY,
        "STATEFP" VARCHAR,
        "COUNTYFP" VARCHAR,
        "TRACTCE" VARCHAR,
        "AFFGEOID" VARCHAR,
        "GEOID" VARCHAR,
        "NAME" VARCHAR,
        "NAMELSAD" VARCHAR,
        "STUSPS" VARCHAR,
        "NAMELSADCO" VARCHAR,
        "STATE_NAME" VARCHAR,
        "LSAD" VARCHAR,
        "ALAND" Numeric,
        "AWATER" Numeric,
        geometry_wkt geometry(Geometry, 4326)
    );
"""

create_crimereports_table = """
    CREATE TABLE IF NOT EXISTS crime_reports (
        "Incident.Number" VARCHAR PRIMARY KEY,
        "Highest.Offense.Description" VARCHAR,
        "Highest.Offense.Code" VARCHAR,
        "Family.Violence" VARCHAR,
        "Ocurred.Date.Time" TIMESTAMP,
        "Ocurred.Date" TIMESTAMP,
        "Ocurred.Time" VARCHAR,
        "Reported.Date.Time" TIMESTAMP,
        "Reported.Date" TIMESTAMP,
        "Reported.Time" VARCHAR,
        "Location.Type" VARCHAR,
        "Address" VARCHAR,
        "Zip.code" VARCHAR,
        "Council.District" VARCHAR,
        "APD.Sector" VARCHAR,
        "APD.District" VARCHAR,
        "PRA" VARCHAR,
        "Census.Tract" VARCHAR,
        "Clearance.Status" VARCHAR,
        "Clearance.Date" VARCHAR,
        "UCR.Category" VARCHAR,
        "Category.Description" VARCHAR,
        "X.coordinate" VARCHAR,
        "Y.coordinate" VARCHAR,
        "Latitude" VARCHAR,
        "Longitude" VARCHAR,
        "Location" VARCHAR
    );
"""

queries_list = [create_extension, create_zipcode_table, create_censustract_table, create_crimereports_table]

for query in queries_list:
    run_query(query)

# https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.2022.html#list-tab-1883739534

# file_zipcode = "cb_2020_us_zcta520_500k.zip"
# blob_zipcode = bucket.blob(file_zipcode)
# content_zipcode = blob_zipcode.download_as_bytes()
# df_zipcode = gpd.read_file(BytesIO(content_zipcode))

# df_zipcode["id"] = range(1, len(df_zipcode) + 1)
# df_zipcode = df_zipcode[["id"] + [col for col in df_zipcode.columns if col != "id"]]
# df_zipcode = df_zipcode.rename(columns={"NAME20": "zip_code"})

# df_zipcode["geometry_wkt"] = df_zipcode["geometry"].apply(lambda geom: geom.wkt)
# df_zipcode.drop(columns=["geometry"], inplace=True)

# https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.2020.html#list-tab-1883739534

# file_censustract = "cb_2022_48_tract_500k.zip"
# blob_censustract = bucket.blob(file_censustract)
# content_censustract = blob_censustract.download_as_bytes()
# df_censustract = gpd.read_file(BytesIO(content_censustract))
# df_censustract["id"] = range(1, len(df_censustract) + 1)
# df_censustract = df_censustract[
#     ["id"] + [col for col in df_censustract.columns if col != "id"]
# ]

# df_censustract["geometry_wkt"] = df_censustract["geometry"].apply(lambda geom: geom.wkt)
# df_censustract.drop(columns=["geometry"], inplace=True)

# df_censustract.to_sql("census_tract", engine, if_exists="append", index= False)






