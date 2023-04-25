# -*- coding: utf-8 -*-
"""    
Created on Fri Mar  3 15:26:58 2023

@author: cc743
"""

## This script processes the updated Domoic Acid (DA) Monitoring data by
## using a threshold for Domoic Acid concentrations to determine "Domoic Acid" event
## then aggregating the data by sample week and county,
## adding a column to indicate "Domoic Acid Week" 
## then aggregating the data agan by county to sum total Domoic Acid Weeks between 2005 and 2020
## then add for counties the spatial data to create a shapefile for ArcGIS.

import pandas as pd
import geopandas as gpd
import numpy as np
import os

os.chdir("V:\\HAB_Hotspot\\Scripts") # current working directory should be the Scripts folder

demog_dir = "..\\Data\\Raw\\CA_demog" # Access shapefile
proc_da_dir = "..\\Data\\Processed\\Processed_DA" # Store processed and aggregated DA data
proc_da_gpd_dir = "..\\Data\\Processed\\Shapefiles" # Store shapefile of DA data

# Open the updated DA data
df_DA = pd.read_csv(os.path.join(proc_da_dir,"df_DA_updated.csv"))

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
    ( (df_DA["Sample Type"].str.contains("Dungeness, viscera") == False) & (df_DA["ASP -ug/g-"] > 20) ), 1, 0) 

df_DA = df_DA.drop(columns = ["Unnamed: 0", "Mod-ASP", "ASP -ug/g-"])

# Save this DA as processed
df_DA.to_csv(os.path.join(proc_da_dir,"df_DA_processed.csv"))
#***this csv shows each individual sample and includes whether the DA concentrations exceed a 20ppm or 30ppm threshold, the management zone in which it falls, and the county in which it falls in/

#%% Aggregate the data by week and county, and calculate Domoic Acid Week (week in a given county where at least one Domoic Acid Event observed)
# Sum up the number of Domoic Acid weeks by county

# Select the date range to match Chlorophyll-a data
df_DA_sub = df_DA.loc[df_DA["Date -Sampled-"].between("2005-01-01", "2020-12-31")]

# Aggregate the individual samples county, summing up the number of DA events (where DA [] exceed 20ppm or 30ppm)
df_county = df_DA_sub.groupby(["County", "Sample Week", "Sample Year"]).agg({"DA Event":["sum","count"]}).reset_index()#.drop(["ASP -ug/g-", "Latitude", "Longitude"], axis = 1)
df_county.columns = df_county.columns.droplevel()
df_county = df_county.set_axis(["County", "Sample Week", "Sample Year", "DA Event", "# Samples"], axis=1, inplace=False)

# Add a column to indicate a Domoic Acid week (weeks where at least 1 DA event was observed)
df_county["DA Week"] = np.where(df_county["DA Event"] > 0, 1, 0)

# Aggregate the number of DA weeks and DA events by county
df_county = df_county.groupby(["County"]).agg({"DA Event":"sum", "# Samples": "sum", "DA Week":["sum", "count"]}).reset_index()
df_county.columns = df_county.columns.droplevel()
df_county = df_county.set_axis(["County", "DA Event", "# Samples", "DA Week", "# Weeks Sampled"], axis=1, inplace=False)
df_county["Proportion DA Weeks"] = df_county["DA Week"]/df_county["# Weeks Sampled"]
df_county.to_csv(os.path.join(proc_da_dir,"df_DA_summary_cnty.csv"))

#***this df shows the total number of DA events and DA weeks observed in a county from 2005-2020
#%% UNUSED Add the geometry of CA Counties to the aggregated data

# Add spatial data useing TIGER files for CA Counties
# EPSG for counties is 3857
counties_gpd = gpd.read_file(os.path.join(demog_dir, "CA_Counties\\CA_Counties_TIGER2016.shp"))

# Merge spatial data with the county aggregate data
df_county = gpd.GeoDataFrame(df_county.merge(counties_gpd, left_on="County", right_on="NAME"))[["County", "DA Event","DA Week", "Proportion DA Weeks", "geometry"]]

df_county.to_file(os.path.join(proc_da_gpd_dir,"df_DA_aggregated_cnty.shp"))

