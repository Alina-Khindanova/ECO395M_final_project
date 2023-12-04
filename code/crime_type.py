import os
import pandas as pd

from database import engine

create_crime_type_table = """
    CREATE TABLE IF NOT EXISTS crime_type (
        id Highest Offense Code,
        "Highest Offense Description" VARCHAR,
        "crime_type" VARCHAR
    );
"""

engine.connect().exec_driver_sql(create_crime_type_table)

df_crime_type.to_sql("crime_type", engine, if_exists="append", index= False)


IN_PATH = os.path.join(
    "data", "Crime_Reports.csv"
)
OUTPUT_DIR = "artifacts"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "Crime_Type.csv")


if __name__ == "__main__":
    # select years: 2011-2022
    df = pd.read_csv(IN_PATH)
    df["Occurred Date"] = pd.to_datetime(df["Occurred Date"])
    df_year = df[
        (df["Occurred Date"] >= "2011-01-01") & (df["Occurred Date"] <= "2022-12-31")
    ]

    df_year = df_year[["Highest Offense Description", "Highest Offense Code"]]

    # Count and print the number of rows in the filtered DataFrame
    num_rows = len(df_year)
    print(f"Number of rows in the filtered data: {num_rows}")
    # 1293921

    # number of Highest Offense Description: 399
    total_distinct_count = df_year[['Highest Offense Description']].nunique().sum()
    print(total_distinct_count)

# mapping
violent_keywords = [
    "FAMILY DISTURBANCE",
    "DATING DISTURBANCE",
    "KIDNAPPING",
    "ASSAULT",
    "TRAFFICKING",
    "RAPE",
    "AGG ASLT STRANGLE/SUFFOCATE",
    "ROBBERY",
    "MURDER",
    "PROTECTIVE ORDER",
    "ROBBERY/DEADLY WEAPON",
    "ASSAULT/FAMILY VIOLENCE",
    "ASSAULT BY THREAT",
    "SEXUAL",
    "ARSON",
    "CRIMINAL MISCHIEF",
    "FELONY ENHANCEMENT/ASSLT W/INJ",
]
property_keywords = [
    "BURGLARY",
    "THEFT",
    "CRIMINAL TRESPASS",
    "BURGLARY OF SHED/DETACHED GARAGE/STORAGE UNIT",
    "HINDERING APPREHENSION",
    "THREAT",
    "DOC EXPOSURE",
    "GRAFFITI",
]
white_collar_keywords = [
    "FRAUD",
    "DEBIT CARD ABUSE",
    "IDENTITY THEFT",
    "MONEY LAUNDERING",
    "FORGERY AND PASSING",
    "FALSE STATEMENT -OBTAIN CREDIT",
    "FALSE REPORT TO PEACE OFFICER",
    "FALSE ALARM OR REPORT",
    "CREDIT CARD ABUSE - OTHER",
    "FORGERY - OTHER",
    "VIOLATION OF BOND CONDITIONS",
]
drug_keywords = [
    "POSS/PROMO CHILD PORNOGRAPHY",
    "POSS OF DRUG PARAPHERNALIA",
    "MARIJUANA",
    "POSS OF PROHIBITED WEAPON",
    "POSS OF GAMBLING PARAPHERNALIA",
    "POSS CONTROLLED SUB/NARCOTIC",
]
cyber_keywords = [
    "ONLINE IMPERSONATION",
    "HARASSMENT ONLINE",
    "BREACH OF COMPUTER SECURITY",
    "SOLICITATION",
    "CONSUMER PROD",
    "TAMPERING WITH EVIDENCE",
    "GOV RECORD",
    "UNLAWFUL INTERCEPTION",
    "SEXTING/TRANSMIT SEXUAL PHOTOS",
]


def categorize_crime(crime_type):
    if any(keyword in crime_type for keyword in violent_keywords):
        return "Violent Crimes"
    elif any(keyword in crime_type for keyword in property_keywords):
        return "Property Crimes"
    elif any(keyword in crime_type for keyword in white_collar_keywords):
        return "White-collar Crimes"
    elif any(keyword in crime_type for keyword in drug_keywords):
        return "Drug-Related Crimes"
    elif any(keyword in crime_type for keyword in cyber_keywords):
        return "Cybercrimes"
    else:
        return "Other"


df_year["crime_type"] = df_year["Highest Offense Description"].apply(categorize_crime)

# distinct highest offense description
df_year_distinct = df_year.drop_duplicates(subset="Highest Offense Description")
df_year_distinct_order = ['Highest Offense Code', 'Highest Offense Description', 'crime_type']
df_year_distinct = df_year_distinct[df_year_distinct_order]

df_year_distinct.to_csv(OUTPUT_PATH, index=False)

print(f"Distinct DataFrame saved to: {OUTPUT_PATH}")


# crime_counts = df_year_distinct["crime_type"].value_counts()

# # Display the counts
# print(crime_counts)

# other_crimes = df_year[df_year["crime_type"] == "Other"]["Highest Offense Description"]

# other_crimes_counts = other_crimes.value_counts()

# # Get the top 15 most common "Other" crime types
# top_15_other_crimes = other_crimes_counts.head(15)

# # Display the top 15 crime types
# print("Top 15 'Other' Crime Types:")
# print(top_15_other_crimes)
