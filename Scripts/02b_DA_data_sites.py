# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 15:50:49 2023

@author: cc743
"""

## This script continues wrangling the Domoic Acid Monitoring data by
## filling the missing sampling location data, the county and 
## the Domoic Acid monitoring zone in which the location resides, and 
## adds geo data to the filled in data

## CA County Data taken from US Census Bureau (2016 data)
    ## https://catalog.data.gov/dataset/tiger-line-shapefile-2016-state-california-current-county-subdivision-state-based
    ## ^Link to TIGER shapefile for CA and data information

import pandas as pd
import os

os.chdir("V:\\HAB_Hotspot\\Scripts") # current working directory should be the Scripts folder

# The following paths are to files that contain more information about the
    # sampling sites and CA demographics (county information)
site_dir = "..\\Data\\Raw\\Free_et_al_Data\\sampling_sites"
demog_dir = "..\\Data\\Raw\\CA_demog"

# This path to collect the combined raw Domoic Acid data and save the 
    # processed Domoic Acid data
proc_da_dir = "..\\Data\\Processed\\Processed_DA"

# Open the combined raw data
df_DA = pd.read_csv(os.path.join(proc_da_dir,"df_DA_samples_DC.csv"))

#%% Fill in the missing lon/lat data for sampling sites
   
# Create a dict of the known sampling locations and their lat/lon coords
lat_dict = dict(zip(df_DA["Sample Site"].dropna(), df_DA["Latitude"].dropna()))
lon_dict = dict(zip(df_DA["Sample Site"].dropna(), df_DA["Longitude"].dropna()))

# Manually find lon/lat data for Sample Sites missing from the dict Long/Lat data
    # looked up on Google the lat/lon for these lat/lon
    # and created a separate .csv
df_b = pd.read_csv(os.path.join(site_dir,"sample-sites-nan.csv"))

# Update the dict item to create a complete dictionary of sampling sites and
    # their lon/lat coords
lat_dict.update(dict(zip(df_b["Sample Site"], df_b["Latitude"])))
lon_dict.update(dict(zip(df_b["Sample Site"], df_b["Longitude"])))

# Use the dict to fill in the missing lon/lat data in the combined raw data
df_DA["Longitude"] = df_DA["Longitude"].fillna(df_DA["Sample Site"].map(lon_dict))
df_DA["Latitude"] = df_DA["Latitude"].fillna(df_DA["Sample Site"].map(lat_dict))

#create a df to collect these dicts
dict_df = pd.DataFrame.from_dict(lat_dict, orient = 'index').reset_index().rename(columns = {"index": "Sample Site", 0: "Latitude"})
dict_df["Longitude"] = dict_df["Sample Site"].map(lon_dict)

#%% Add county data using CA County TIGER files

# Create dictionary of Sample Site and County from raw data
county_dict = dict(zip(df_DA["Sample Site"], df_DA["County"]))

# Fill the nan in the county dict
# Created a new csv to contain the missing county data and sample sites
df_c = pd.read_csv(os.path.join(site_dir,"sample-sites-nan-county.csv"))
county_dict.update(dict(zip(df_c["Sample Site"], df_c["County"])))

# Add county dict to the dictionary df
dict_df["County"] = dict_df["Sample Site"].map(county_dict)

# Fill in missing county data in DA data
df_DA["County"] = df_DA["County"].fillna(df_DA["Sample Site"].map(county_dict))

#%% Add management zone information to DA Data

# Created zone id's based on WC_dcrab_da_mgmt_zones in ../Data/Raw folder
zones = []

for i, data in dict_df.iterrows():
    lat = dict_df.iloc[i]["Latitude"]
    cnty = dict_df.iloc[i]["County"]
    
    if (cnty == "Del Norte"):
        zones.append("A")  
    elif (cnty == "Humboldt") & (lat > 41.2933):
        zones.append("A")
    elif (cnty == "Humboldt") & (lat > 40.1667):
        zones.append("B")
    elif (cnty == "Humboldt") & (lat < 40.1667):
        zones.append("C")
    elif (cnty == "Mendocino") & (lat > 39.555):
        zones.append("C")
    elif (cnty == "Mendocino") & (lat < 39.555):
       zones.append("D")       
    elif (cnty == "Sonoma"):
       zones.append("E") 
    elif (cnty == "Marin") & (lat > 38):
       zones.append("E")     
    elif (cnty == "Marin") & (lat < 38):
       zones.append("F")    
    elif (cnty == "San Francisco") | (cnty == "Alameda"):
       zones.append("F")       
    elif (cnty == "San Mateo") & (lat > 37.1833):
        zones.append("F")
    elif (cnty == "San Mateo") & (lat < 37.1833):
        zones.append("G")    
    elif (cnty == "Santa Cruz"):
        zones.append("G")
    elif (cnty == "Monterey") & (lat > 36):
        zones.append("G")
    elif (lat < 36):
        zones.append("H")
    elif (cnty == "San Luis Obispo") | (cnty == "Santa Barbara") | (cnty == "Ventura") | (cnty == "Los Angeles") | (cnty == "Orange") | (cnty == "San Diego"):
        zones.append("H")
    else: zones.append('Z')

# Zones list shares same order as df_DA
dict_df["Zone"] = zones

# Create zone dictionary for sample sites
zone_dict = dict(zip(dict_df["Sample Site"], dict_df["Zone"]))

# Add Zone data to DA data
df_DA["Zone"] = df_DA["Sample Site"].map(zone_dict)

#%% Add geometry data of County to the DA data

# Save dictionary for QAQC use
#dict_df.to_csv(os.path.join(proc_da_dir, "df_DA_site_dictionary.csv")) #information about the sample sites (coord, county, and zone)

# Save update DA data
df_DA = df_DA.drop(columns = "Unnamed: 0")
df_DA.to_csv(os.path.join(proc_da_dir,"df_DA_updated.csv"))
