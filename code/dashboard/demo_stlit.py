import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import text
from database import engine  

# Function to load data
def load_data():
    # Query to get median household income and percent_bachelors_higher by zipcode from demographics table
    income_query = text("""
    SELECT "zip_code_year", median_household_income, percent_bachelors_higher 
    FROM demographics
    """)
    income_data = pd.read_sql(income_query, engine)

    # Query to get crime count by zipcode and year from crime_reports table
    crime_query = text("""
    SELECT 
    "Zip.code", EXTRACT(YEAR FROM "Ocurred.Date") AS year, COUNT(*) AS crime_count
    FROM crime_reports
    GROUP BY "Zip.code", EXTRACT(YEAR FROM "Ocurred.Date")
    """)
    crime_data = pd.read_sql(crime_query, engine)

    # Creating the zipcode_year variable
    crime_data["zip_code_year"] = crime_data["Zip.code"].astype(str) + "_" + crime_data["year"].astype(int).astype(str)

    return income_data, crime_data

# Load data
income_data, crime_data = load_data()

# Preparing the data for plotting
# Merging the datasets on zip_code_year
merged_data = pd.merge(crime_data, income_data, on="zip_code_year", how="inner")

# Filter out rows where median_household_income or percent_bachelors_higher is -666666688
filtered_data = merged_data.query("median_household_income != -666666688 and percent_bachelors_higher != -666666688")

# Creating the first scatter plot
st.write("Scatter Plot of Median Household Income vs Crime Reports Count")
fig, ax = plt.subplots()
ax.scatter(filtered_data["median_household_income"], filtered_data["crime_count"])
ax.set_xlabel("Median Household Income")
ax.set_ylabel("Crime Reports Count")
ax.set_title("Income vs Crime Reports Count by Zipcode and Year")
st.pyplot(fig)

# Creating the second scatter plot
st.write("Scatter Plot of Percent with Bachelor's Degree or Higher vs Crime Reports Count")
fig2, ax2 = plt.subplots()
ax2.scatter(filtered_data["percent_bachelors_higher"], filtered_data["crime_count"])
ax2.set_xlabel("Percent with Bachelor's Degree or Higher")
ax2.set_ylabel("Crime Reports Count")
ax2.set_title("Education vs Crime Reports Count by Zipcode and Year")
st.pyplot(fig2)