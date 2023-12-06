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


query_1 = """
  SELECT
    hc."Zip.code",
    hc.Year,
    hc.Harassment_Count,
    ot."geometry_wkt"
  FROM (
  SELECT
    "Zip.code",
    EXTRACT(YEAR FROM "Ocurred.Date") AS Year,
    COUNT(*) AS Harassment_Count
  FROM
    crime_reports
  WHERE
    "Highest.Offense.Description" = 'HARASSMENT'
  GROUP BY
    "Zip.code",
  EXTRACT(YEAR FROM "Ocurred.Date")
)   hc
  JOIN
    zipcode ot ON hc."Zip.code" = ot."zip_code";
"""
gdf = gpd.read_postgis(query_1, engine, geom_col="geometry_wkt")

gdf["year"] = gdf["year"].round(0).astype(int)


def create_choropleth_map(gdf, year):
    gdf_year = gdf[gdf["year"] == year]

    subset_json_with_id = gdf_year.set_index(keys="Zip.code").to_json()

    m = folium.Map(location=[30.2422346, -97.7660421], zoom_start=10)

    choropleth = folium.Choropleth(
        geo_data=subset_json_with_id,
        name="choropleth",
        data=gdf_year,
        columns=["Zip.code", "harassment_count"],
        key_on="feature.id",
        fill_color="YlOrRd",  
        fill_opacity=0.9,  
        line_opacity=0.2,
        legend_name="Harassment Count",
    ).add_to(m)

    choropleth.geojson.add_to(m)

    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['harassment_count'], labels=False)
    )

    folium.LayerControl().add_to(m)

    return m


def main():
    st.title("Interactive Map of Harassment Count per Year")

    total_harassment_count = gdf["harassment_count"].sum()

    col1, col2 = st.columns([2, 1])

# In the first column, display your map
    col1.subheader("Harassment Count for Selected Year")
        
    selected_year = col1.slider(
        "Select Year",
        min_value=int(gdf["year"].min()),
        max_value=int(gdf["year"].max()),
    )
    mymap = create_choropleth_map(gdf, selected_year)
    folium_static(mymap, width=400, height=450)

    col2.subheader("Total Harassment Count for Selected Year")
    col2.write(f"{total_harassment_count} incidents")


if __name__ == "__main__":
    main()
