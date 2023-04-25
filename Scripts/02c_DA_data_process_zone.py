# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 12:53:57 2023

@author: cc743
"""

## This script processes the updated Domoic Acid (DA) Monitoring data by
## using a threshold for Domoic Acid concentrations to determine "Domoic Acid" event
## then aggregating the data by sample week and county,
## adding a column to indicate "Domoic Acid Week" 
## then aggregating the data agan by management zone to get the proportion
## of sample weeks observing Domoic Acid Events between 2005 and 2020
## then add for management zones the spatial data to create a shapefile for ArcGIS.

import pandas as pd
import geopandas as gpd
import numpy as np
import os

os.chdir("V:\\HAB_Hotspot\\Scripts") # current working directory should be the Scripts folder

demog_dir = "..\\Data\\Raw\\CA_demog" # Access shapefile
proc_dir = "..\\Data\\Processed" # Store the custom-made shapefile for management zones
proc_da_dir = "..\\Data\\Processed\\Processed_DA" # Store processed and aggregated DA data
geo_dir = "..\\Data\\Processed\\Shapefiles" # Save the shapefile
arc_dir = "..\\Data\\Processed\\For_ArcGIS" # Save clipped copy of shapefile for mapmaking

# Open the updated DA data
df_DA = pd.read_csv(os.path.join(proc_da_dir,"df_DA_updated.csv"))

#%% Create management zones

# Create spatial area for management zones
state = gpd.read_file(os.path.join(demog_dir, "CA_State\\CA_State_TIGER2016.shp"))

# Create polygons that cover management zones (zone boundaries in Raw/management zones.csv)
from shapely.geometry import Polygon

# Create a polygon with the desired dimensions of the map
A = Polygon([(-130, 42.0000000), (-110, 42.0000000), (-110, 41.2933333), (-130, 41.2933333)])
B = Polygon([(-130, 41.2933333), (-110, 41.2933333), (-110, 40.1666667), (-130, 40.1666667)])
C = Polygon([(-130, 40.1666667), (-110, 40.1666667), (-110, 39.5550000), (-130, 39.5550000)])
D = Polygon([(-130, 39.5550000), (-110, 39.5550000), (-110, 38.7687500), (-130, 38.7687500)])
E = Polygon([(-130, 38.7687500), (-110, 38.7687500), (-110, 38.0000000), (-130, 38.0000000)])
F = Polygon([(-130, 38.0000000), (-110, 38.0000000), (-110, 37.1833333), (-130, 37.1833333)])
G = Polygon([(-130, 37.1833333), (-110, 37.1833333), (-110, 36.0000000), (-130, 36.0000000)])
H = Polygon([(-130, 36.0000000), (-110, 36.0000000), (-110, 32.5343430), (-130, 32.5343430)])

zones = {"Zone": ["A", "B", "C", "D", "E", "F", "G","H"], 
         "geometry": [A, B, C, D, E, F, G, H]}

zone_gpd = gpd.GeoDataFrame(zones,crs = 4326, geometry = zones["geometry"])
zone_gpd = zone_gpd.to_crs('EPSG:3857')

zone_gpd = state.overlay(zone_gpd, how = 'intersection')
zone_gpd.to_file(os.path.join(proc_dir, "Processed_mgt_zones\\CA_mgt_zones"))

#%% Convert datetime column to Sample Week, Sample Month, and Sample Year

df_DA["Date -Sampled-"] = pd.to_datetime(df_DA["Date -Sampled-"])
df_DA["Sample Week"] = df_DA["Date -Sampled-"].dt.isocalendar().week.astype(int)
df_DA["Sample Month"] = df_DA["Date -Sampled-"].dt.month.astype(int)
df_DA["Sample Year"] = df_DA["Date -Sampled-"].dt.year.astype(int)

#%% Add a column to represent DA Events, which occurs in one of two ways:
# when Domoic Acid is greater than 20 ug/g
# when Domoic Acid in Dungeness Crab, viscera is greater than 30 ug/g

# Add a column to represent a Domoic Acid event
df_DA["DA Event"] = np.where( 
    ( (df_DA["Sample Type"].str.contains("Dungeness, viscera")) & (df_DA["ASP -ug/g-"] > 30) ) | 
    ( (df_DA["Sample Type"].str.contains("Dungeness, viscera") == False) & (df_DA["ASP -ug/g-"] > 20) ), 1, 0) #assume all other data not viscera samples

df_DA = df_DA.drop(columns = ["Unnamed: 0", "Mod-ASP", "ASP -ug/g-"])

# Save this DA as processed
df_DA.to_csv(os.path.join(proc_da_dir,"df_DA_processed.csv"))
#***this csv shows each individual sample and includes whether the DA concentrations exceed a 20ppm or 30ppm threshold, the management zone in which it falls, and the county in which it falls in/

#%% Aggregate the DA data by management zones

# Aggregate the individual samples by week and zone, summing up the number of DA events (where DA [] exceed 20ppm or 30ppm)
df_zone = df_DA.groupby(["Zone", "Sample Week", "Sample Year"]).agg({"DA Event":["sum", "count"]}).reset_index()#.drop(["ASP -ug/g-", "Latitude", "Longitude"], axis = 1)
df_zone.columns = df_zone.columns.droplevel()
df_zone = df_zone.set_axis(["Zone", "Sample Week", "Sample Year", "DA Event", "# Samples"], axis=1, inplace=False)

# Add a column to indicate a Domoic Acid week (weeks where at least 1 DA event was observed)
df_zone["DA Week"] = np.where(df_zone["DA Event"] > 0, 1, 0)

# Aggregate the number of DA weeks and DA events by zone
df_zone = df_zone.groupby(["Zone"]).agg({"DA Event":"sum", "# Samples": "sum", "DA Week":["sum", "count"]}).reset_index()
df_zone.columns = df_zone.columns.droplevel()
df_zone = df_zone.set_axis(["Zone", "DA Event", "# Samples", "DA Week", "# Weeks Sampled"], axis=1, inplace=False)
df_zone["Proportion DA Weeks"] = df_zone["DA Week"]/df_zone["# Weeks Sampled"]
df_zone.to_csv(os.path.join(proc_da_dir,"df_DA_summary_zone.csv"))

# Merge spatial and DA data; CRS should be EPSG:3857
df_DA_zone_agg = gpd.GeoDataFrame(df_zone.merge(zone_gpd, on="Zone"))
df_DA_zone_agg = df_DA_zone_agg[["Zone", "DA Event", "# Samples", "DA Week", "# Weeks Sampled", "Proportion DA Weeks", "geometry"]]
df_DA_zone_agg.to_file(os.path.join(geo_dir,"df_DA_zone_agg.shp")) # sum of weekly DA events for each county

#%% Clip the DA shapefile to CA boundary

import arcpy 
import os

# Arc Set up
arcpy.env.workspace = arc_dir
arcpy.env.extent = "-127.499997461121 32.5342903 -114.999994909484 42.000000772404"
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("WGS 1984")

# Clip using online Feature Layer by Brian Shaw
mask = "https://services2.arcgis.com/C8EMgrsFcRFL6LrL/arcgis/rest/services/US_States_and_Territories/FeatureServer/0"
da_clip = arcpy.analysis.Clip(os.path.join(geo_dir,"df_DA_zone_agg.shp"), mask)

                            
