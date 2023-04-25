# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 12:59:24 2023

@author: cc743
"""

import pandas as pd
import geopandas as gpd
import numpy as np
import os

site_dir = "..\\Data\\Raw\\Free_et_al_Data\\sampling_sites"
proc_da_dir = "..\\Data\\Processed\\Processed_DA"
ts_dir = "..\\Data\\Processed\\Time_Series"

df_DA = pd.read_csv(os.path.join(proc_da_dir,"df_DA_processed.csv"))

#%%
#fill in zone, county, lat, lon data 
df_sites = pd.read_csv(os.path.join(proc_da_dir,"df_DA_sites.csv"))

key = df_sites["Sample Site"]
zone_dict = dict(zip(key, df_sites["Zone"]))
count_dict= dict(zip(key, df_sites["County"]))
lat_dict= dict(zip(key, df_sites["Latitude"]))
long_dict= dict(zip(key, df_sites["Longitude"]))

#%% create blank time series df

#every sample point, based on Free et al data
point_unique = list(df_DA["Sample Site"].unique())

point_full = []
yr_full = []
month_full = []
wk_full = []

for i in point_unique:
    for j in range(2000, 2022):
        for l in range(1, 54):
            point_full.append(str(i))
            yr_full.append(str(j))
            wk_full.append(str(l))

time_point_df = pd.DataFrame({"Sample Site" : point_full, "Sample Year" : yr_full, "Sample Week" : wk_full})
#time_point_df = time_point_df.astype({'Sample Week':'int', "Sample Year": "int"})
time_point_df["Date"] = time_point_df["Sample Year"].astype('int')*100 + time_point_df["Sample Week"].astype('int')
time_point_df["Date"] = pd.to_datetime(time_point_df["Date"].astype('str') + '0', format = '%Y%W%w')
time_point_df["Month"] = time_point_df["Date"].dt.month.astype(int)
time_point_df["Sample Year"] = time_point_df["Sample Year"].astype('int')
time_point_df["Sample Week"] = time_point_df["Sample Week"].astype('int')

time_point_df["Zone"] = time_point_df["Sample Site"].map(zone_dict)
time_point_df["County"] = time_point_df["Sample Site"].map(count_dict)
time_point_df["Latitude"] = time_point_df["Sample Site"].map(lat_dict)
time_point_df["Longitude"] = time_point_df["Sample Site"].map(long_dict)

#%% aggregate data by Sample Week
df_DA_week = df_DA.groupby(["Sample Site", "Sample Week", "Sample Year", "County", "Zone"]).agg({'DA_event': 'sum', "Latitude":"mean", "Longitude": 'mean', "Sample Month": "mean"}).reset_index()

df_DA_full = time_point_df.merge(df_DA_week, left_on = ["Sample Week", "Sample Year", "Sample Site"], right_on=["Sample Week", "Sample Year", "Sample Site"], how = "outer").drop(columns = ["Longitude_y","Latitude_y"])
df_DA_full= df_DA_full.drop(columns = ["County_y", "Zone_y", "Sample Month"]).rename(
    columns = {"Zone_x": "Zone",
               "County_x": "County",
               "Latitude_x": "Latitude",
               "Longitude_x": "Longitude"})

df_DA_full["DA_event"] = df_DA_full["DA_event"].fillna(0)
df_DA_full["DA_week"] = np.where(df_DA_full["DA_event"] > 0 , 1, 0)
df_DA_full.to_csv(os.path.join(ts_dir,"df_DA_week.csv")) #for time series analysis for later (can groupby zone or county)

#%% aggregate the individual samples by week and county, summing up the number of DA events (where DA [] exceed 20ppm or 30ppm)
df_DA_county = df_DA_full.groupby(["County", "Sample Week", "Sample Year"]).agg({"DA_event":"sum", "DA_week": "sum"}).reset_index()#.drop(["ASP -ug/g-", "Latitude", "Longitude"], axis = 1)

#pivot to observe all management zones at once for a given sample week
df_DA_county_pivot = df_DA_county.pivot(index = ["Sample Year", "Sample Week"], columns = "County", values = ["DA_event", "DA_week"])
df_DA_county_pivot.to_csv(os.path.join(ts_dir,"df_DA_county_week_pivot.csv"))

#%% aggregate the individual samples by week and county, summing up the number of DA events (where DA [] exceed 20ppm or 30ppm)
df_DA_zone = df_DA_full.groupby(["Zone", "Sample Week", "Sample Year"]).agg({"DA_event":"sum", "DA_week": "sum"}).reset_index()#.drop(["ASP -ug/g-", "Latitude", "Longitude"], axis = 1)

#pivot to observe all management zones at once for a given sample week
df_DA_zone_pivot = df_DA_zone.pivot(index = ["Sample Year", "Sample Week"], columns = "Zone", values = ["DA_event", "DA_week"])
df_DA_zone_pivot.to_csv(os.path.join(ts_dir,"df_DA_zone_week_pivot.csv"))
