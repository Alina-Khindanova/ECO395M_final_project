import os
import pandas as pd

from database import engine

drop_table = """
DROP TABLE IF EXISTS crime_type
"""
create_crime_type_table = """
    CREATE TABLE IF NOT EXISTS crime_type (
        "Highest.Offense.Code" SERIAL PRIMARY KEY,
        "Highest.Offense.Description" VARCHAR,
        "crime.type" VARCHAR
    );
"""

query_offense_data = """
SELECT 
    "Highest.Offense.Code",
    "Highest.Offense.Description",
    "Ocurred.Date"
FROM
    crime_reports
WHERE
    "Ocurred.Date" BETWEEN '2011-01-01' AND '2022-12-31';
"""

engine.connect().exec_driver_sql(drop_table)
engine.connect().exec_driver_sql(create_crime_type_table)

df_crime_type = pd.read_sql_query(query_offense_data, engine)

# print(df_crime_type.shape) # total 1293921 data


if __name__ == "__main__":
    # number of Highest Offense Description: 399
    total_distinct_count = (
        df_crime_type[["Highest.Offense.Description"]].nunique().sum()
    )
    # print(total_distinct_count)

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
    "SEX",
    "FELONY ENHANCEMENT/ASSLT W/INJ",
    "SODOMY",
    "STRANGL",
    "INJURY",
    "PROSTITUTION",
    "INDECENCY WITH A CHILD/CONTACT",
    "INDECENT EXPOSURE",
    "ENTICING A CHILD",
    "CONT SEX ABUSE OF CHILD",
    "INDECENCY WITH CHILD/EXPOSURE",
    "CHILD ENDANGERMENT-ABANDONMENT",
    "VIOL",
    "RESTRAINT",
    "HINDER",
    "WEAPON",
    "GAMBLING PARAPHERNALIA",
]
property_keywords = [
    "BURGLARY",
    "THEFT",
    "CRIMINAL TRESPASS",
    "BURGLARY OF SHED/DETACHED GARAGE/STORAGE UNIT",
    "GRAFFITI",
    "BURG OF RES - FAM/DATING ASLT",
    "DAMAGE",
    "PURSE SNATCHING",
    "ARSON",
    "CRIMINAL MISCHIEF",
    "RENTAL CAR/FAIL TO RETURN",
    "TAMPERING WITH EVIDENCE",
]
white_collar_keywords = [
    "FRAUD",
    "DEBIT CARD ABUSE",
    "IDENTITY THEFT",
    "MONEY LAUNDERING",
    "FORGERY AND PASSING",
    "FALSE STATEMENT -OBTAIN CREDIT",
    "CREDIT CARD ABUSE - OTHER",
    "FORGERY - OTHER",
    "FORGERY OF IDENTIFICATION",
    "COUNTERFEITING",
    "FICTITIOUS",
    "FORGERY",
    "BANK KITING",
    "BRIBERY",
    "PERJURY",
    "MISAPPLY FIDUCIARY PROP",
    "MISUSE OF OFFICIAL INFO",
    "POSSESSION OF FORGED WRITING",

]
drug_keywords = [
    "DRUG",
    "MARIJUANA",
    "CONTROLLED",
    "ALCOHOL",
    "DWI",
    "DANG DRUG",
    "DXM",
]
cyber_keywords = [
    "ONLINE IMPERSONATION",
    "BREACH OF COMPUTER SECURITY",
    "GOV RECORD",
    "UNLAWFUL INTERCEPTION",
    "SEXTING/TRANSMIT SEXUAL PHOTOS",
    "COMMUNICATING",
    "FALSE",
    "TELECOMMUNICATION",
    "DISCLOSE/PROMO INTIMATE VISUA",
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


df_crime_type["crime.type"] = df_crime_type["Highest.Offense.Description"].apply(
    categorize_crime
)

# distinct highest offense description
df_crime_type_distinct = df_crime_type.drop_duplicates(
    subset="Highest.Offense.Code"
) ##362 distinct code
df_crime_type_distinct_order = [
    "Highest.Offense.Code",
    "Highest.Offense.Description",
    "crime.type",
]

df_crime_type_distinct = df_crime_type_distinct[df_crime_type_distinct_order]


df_crime_type_distinct.to_sql("crime_type", engine, if_exists="append", index=False)

# crime_counts = df_crime_type_distinct["crime.type"].value_counts()

# # Display the counts
# print(crime_counts)

# other_crimes = df_crime_type[df_crime_type["crime.type"] == "Other"][
#     "Highest.Offense.Description"
# ]

# print(other_crimes)
# other_crimes_counts = other_crimes.value_counts()

# # Get the top 15 most common "Other" crime types
# top_15_other_crimes = other_crimes_counts.head(15)

# # Display the top 15 crime types
# print("Top 15 'Other' Crime Types:")
# print(top_15_other_crimes)
