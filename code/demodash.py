import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import json
from streamlit_folium import folium_static
from database import engine


def create_choropleth_map(gdf, year, crime_t):
    """Provide a data frame, a year and a crime type to get a choropleth map"""

    gdf_year_type = gdf[(gdf["year"] == year) & (gdf["crime.type"] == crime_t)]

    # Create a geojson object to feed the map
    subset_json_with_id = gdf_year_type.set_index(keys="Zip.code").to_json()

    m = folium.Map(location=[30.2572346, -97.7260421], zoom_start=10)

    choropleth = folium.Choropleth(
        geo_data=subset_json_with_id,
        name="choropleth",
        data=gdf_year_type,
        columns=["Zip.code", "crime_count"],
        key_on="feature.id",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.3,
        legend_name="Crime Count",
    ).add_to(m)

    choropleth.geojson.add_to(m)

    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(["name_zip", "crime_count"], labels=False)
    )

    folium.LayerControl().add_to(m)

    return m


def main():
    st.set_page_config(layout="wide")

    st.markdown(
        "<h1 style='text-align: center;'>Austin: Insights into 2011-2023 Crime Data</h1>",
        unsafe_allow_html=True,
    )

    col1, space, col2 = st.columns([3, 0.25, 3])

    # Elements in colum 1 of the dashboard

    query_crime_time_series = """
      SELECT
        ct."crime.type",
        TO_CHAR(cr."Ocurred.Date", 'YYYYMM') AS year_month,
        COUNT(*) AS crime_count
      FROM
        crime_reports cr
      JOIN
        crime_type ct ON cr."Highest.Offense.Description" = ct."Highest.Offense.Description"
      WHERE
        cr."Ocurred.Date" >= '2011-01-01'  -- Adjust the start date as needed
      GROUP BY
        ct."crime.type",
      TO_CHAR(cr."Ocurred.Date", 'YYYYMM')
      ORDER BY
        ct."crime.type",
        year_month;
    """

    df_ts = pd.read_sql(query_crime_time_series, engine)

    df_ts["year_month"] = pd.to_datetime(df_ts["year_month"], format="%Y%m")

    df_ts_filtered = df_ts[df_ts["year_month"] <= "2023-10-01"]

    # Include the average number of crime reports per year to the dashboard
    sum_crime_count_per_year = (
        df_ts_filtered.groupby(df_ts_filtered["year_month"].dt.year)["crime_count"]
        .sum()
        .reset_index(name="sum_crime_count")
    )

    average_crime_count_overall = int(
        sum_crime_count_per_year["sum_crime_count"].mean()
    )

    col1.markdown(
        f"##### Average number of crime reports per year: {average_crime_count_overall:,.0f}"
    )

    # Include type of crime participation to the dashboard
    crime_count_per_type = (
        df_ts_filtered.groupby("crime.type")["crime_count"]
        .sum()
        .reset_index(name="total_crime_count")
    )

    crime_count_per_type["percentage"] = (
        crime_count_per_type["total_crime_count"]
        / crime_count_per_type["total_crime_count"].sum()
    ) * 100

    col1.markdown("##### Type of crime participation")

    bullets = [
        f"- {row['crime.type']}: {row['percentage']:.1f}%"
        for index, row in crime_count_per_type.iterrows()
    ]
    col1.text("\n".join(bullets))

    # Include a graph of the evolution of crime reports between 2011 and 2023 per type of crime
    col1.markdown(
        "<h2 style='text-align: center;'>Number of crime reports per month</h2>",
        unsafe_allow_html=True,
    )

    fig, ax = plt.subplots(figsize=(14, 9))

    for crime_type, group_df in df_ts_filtered.groupby("crime.type"):
        (original_line,) = ax.plot(
            group_df["year_month"],
            group_df["crime_count"],
            label=f"{crime_type}",
            linewidth=2.5,
        )
        smoothed_line = group_df["crime_count"].rolling(window=12, min_periods=1).mean()
        lighter_color = sns.desaturate(original_line.get_color(), 0.5)
        ax.plot(
            group_df["year_month"], smoothed_line, linestyle="--", color=lighter_color
        )

    plt.xticks(rotation=90, ha="right")

    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.13),
        ncol=2,
        prop={"size": 20},
        handlelength=2.0,
    )

    ax.tick_params(axis="both", which="major", labelsize=20)

    col1.pyplot(fig, clear_figure=True)

    # Include a scatterplot of Income vs Crime Reports Count by Zipcode and Year

    income_query = """
      SELECT 
        "zip_code_year", 
        median_household_income, 
        percent_bachelors_higher 
      FROM 
        demographics
    """
    crime_query = """
      SELECT 
        "Zip.code", 
        EXTRACT(YEAR FROM "Ocurred.Date") AS year, 
        COUNT(*) AS crime_count
      FROM 
        crime_reports
      GROUP BY 
        "Zip.code", EXTRACT(YEAR FROM "Ocurred.Date")
    """
    income_data = pd.read_sql(income_query, engine)

    crime_data = pd.read_sql(crime_query, engine)

    crime_data["zip_code_year"] = (
        crime_data["Zip.code"].astype(str)
        + "_"
        + crime_data["year"].astype(int).astype(str)
    )

    merged_data = pd.merge(crime_data, income_data, on="zip_code_year", how="inner")

    filtered_data = merged_data.query(
        "median_household_income != -666666688 and percent_bachelors_higher != -666666688"
    )

    col1.markdown(
        "<h4 style='text-align: center;'>Income vs Crime Reports Count by Zipcode and Year</h4>",
        unsafe_allow_html=True,
    )

    fig, ax = plt.subplots()
    ax.scatter(filtered_data["median_household_income"], filtered_data["crime_count"])
    ax.set_xlabel("Median Household Income")
    ax.set_ylabel("Crime Reports Count")
    col1.pyplot(fig, clear_figure=True)

    # Elements in colum 2 of the dashboard

    # Include interactive map of crime types and years

    query_interactive_map = """
      SELECT
        EXTRACT(YEAR FROM cr."Ocurred.Date") AS year,
        ct."crime.type",
        cr."Zip.code",
        cr."Zip.code" as name_zip,
        zc.geometry_wkt,
        COUNT(*) AS crime_count
      FROM
        crime_reports cr
      JOIN
        crime_type ct ON cr."Highest.Offense.Description" = ct."Highest.Offense.Description"
      JOIN
        zipcode zc ON cr."Zip.code" = zc.zip_code
      WHERE
        cr."Zip.code" IS NOT NULL AND cr."Zip.code" <> '0'
        AND EXTRACT(YEAR FROM cr."Ocurred.Date") > 2010
      GROUP BY
        year, ct."crime.type", cr."Zip.code", zc.geometry_wkt;
    """
    gdf = gpd.read_postgis(query_interactive_map, engine, geom_col="geometry_wkt")

    gdf["year"] = gdf["year"].round(0).astype(int)

    crime_list = list(gdf["crime.type"].unique())
    crime_list.sort()

    selected_crime = col2.selectbox("Crime Type", crime_list)

    selected_year = col2.selectbox(
        "Select Year",
        options=range(int(gdf["year"].min()), int(gdf["year"].max()) + 1),
        index=0,
    )

    col2.markdown(
        f"<h2 style='text-align: center;'>{selected_crime} per Zip Code in {selected_year}</h2>",
        unsafe_allow_html=True,
    )

    with col2:
        mymap = create_choropleth_map(gdf, selected_year, selected_crime)
        folium_static(mymap, width=590, height=490)

    # Include a scatterplot of Education vs Crime Reports Count by Zipcode and Year

    col2.markdown(
        "<h4 style='text-align: center;'>Education vs Crime Reports Count by Zipcode and Year</h4>",
        unsafe_allow_html=True,
    )

    fig2, ax2 = plt.subplots()
    ax2.scatter(filtered_data["percent_bachelors_higher"], filtered_data["crime_count"])
    ax2.set_xlabel("Percent with Bachelor's Degree or Higher")
    ax2.set_ylabel("Crime Reports Count")
    col2.pyplot(fig2, clear_figure=True)


if __name__ == "__main__":
    main()
