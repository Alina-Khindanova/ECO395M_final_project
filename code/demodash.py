import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium, folium_static
from folium.plugins import HeatMap, MarkerCluster
from database import engine
from shapely import wkt
from shapely.geometry import shape
import shapely
import json
import matplotlib.pyplot as plt
import seaborn as sns

def create_choropleth_map(gdf, year, crime_t):
    
    gdf_year_type = gdf[(gdf["year"] == year) & (gdf["crime.type"] == crime_t)]

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
        folium.features.GeoJsonTooltip(["name_zip",'crime_count'], labels=False)
    )

    folium.LayerControl().add_to(m)

    return m


def main():
    st.set_page_config(layout="wide")
    st.markdown("<h1 style='text-align: center;'>Austin Crime Dashboard</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 3])

    # Column 1 graph 
    col1.markdown("<h2 style='text-align: center;'>Monthly incidences</h2>", unsafe_allow_html=True)
    
    query_crime_series="""
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
    
    df_ts = pd.read_sql(query_crime_series, engine)

    df_ts['year_month'] = pd.to_datetime(df_ts['year_month'], format='%Y%m')

    df_ts_filtered = df_ts[df_ts['year_month'] <= '2023-10-01']

    fig, ax = plt.subplots(figsize=(16, 10))

    for crime_type, group_df in df_ts_filtered.groupby('crime.type'):
        original_line, = ax.plot(group_df['year_month'], group_df['crime_count'], label=f'{crime_type}',linewidth=2.5)
        smoothed_line = group_df['crime_count'].rolling(window=12, min_periods=1).mean()
        lighter_color = sns.desaturate(original_line.get_color(), 0.5)
        ax.plot(group_df['year_month'], smoothed_line, linestyle='--', color=lighter_color)

    plt.xticks(rotation=90, ha='right')

    ax.legend(
            loc='upper center',
            bbox_to_anchor=(0.5, -0.13),
            ncol=2,
            prop={'size':20 },
            handlelength=2.0 
        )
    
    ax.tick_params(axis='both', which='major', labelsize=20)

    col1.pyplot(fig, clear_figure=True)

    # Column 2 graph 
    query_map = """
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
    gdf = gpd.read_postgis(query_map, engine, geom_col="geometry_wkt")

    gdf["year"] = gdf["year"].round(0).astype(int)
    
    crime_list = list(gdf['crime.type'].unique())
    crime_list.sort() 

    selected_crime = col2.selectbox('Crime Type', crime_list)

    selected_year = col2.selectbox(
        "Select Year",
        options=range(int(gdf["year"].min()), int(gdf["year"].max()) + 1),
        index=0
    )
    
    col2.markdown(f"<h2 style='text-align: center;'>{selected_crime} per Zip Code</h2>", unsafe_allow_html=True)

    with col2:
        mymap = create_choropleth_map(gdf, selected_year,selected_crime)
        folium_static(mymap, width=590, height=400)


if __name__ == "__main__":
    main()