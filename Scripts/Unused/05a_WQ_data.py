# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 14:20:40 2023

@author: cc743
"""

#%%
import pandas as pd
import numpy as np
import os
import re 

raw_wq_path = "../Data/Raw/Cha_Obrien_Data"
raw_wq = os.listdir(raw_wq_path)

#take out location information for the location-based csvs
locs = [re.findall("(?<=HABs-).*", re.split("_", str)[0])[0] for str in raw_wq]
wq_files = [pd.read_csv(os.path.join(raw_wq_path, f)).iloc[1:] for f in raw_wq] 

#take out the pre2019 df as it covers multiple locations
pre2019 = wq_files[3]
pre2019["coord"] = pre2019[["latitude", "longitude"]].apply(", ".join, axis = 1) #missing location info, but have location code
coords = dict(zip(pre2019["coord"], pre2019["Location_Code"])) #dict used to map location code to location-based dfs

# concat the location-based dfs int post 2019 df
wq_concat = []

for i in range(len(wq_files)):
    if locs[i] == "pre20190601": pass
    else:
        j = wq_files[i]
        j["loc"] = locs[i]
        j["coord"] = j[["latitude", "longitude"]].apply(", ".join, axis = 1)
        j["Location_Code"] = j["coord"].map(coords)
        wq_concat.append(j)
        
post2019 = pd.concat(wq_concat)

#create dict of loc codes and locations to map the pre2019 df
loc_codes = dict(zip(post2019["Location_Code"], post2019["loc"]))
loc_codes["GP"] = "GoletaPier"
loc_codes["TP"] = "TrinidadPier"

pre2019["loc"] = pre2019["Location_Code"].map(loc_codes)

#combine pre2019 and post2019 into wq_df
wq_df = pd.concat([post2019, pre2019])
cols_to_float = ['latitude', 'longitude', 'depth',
       'Temp', 'Air_Temp', 'Salinity', 'Chl_Volume_Filtered', 'Chl1', 'Chl2',
       'Avg_Chloro', 'Phaeo1', 'Phaeo2', 'Avg_Phaeo', 'Phosphate', 'Silicate',
       'Nitrite', 'Nitrite_Nitrate', 'Ammonium', 'Nitrate',
       'DA_Volume_Filtered', 'pDA', 'tDA', 'dDA',
       'Volume_Settled_for_Counting', 'Akashiwo_sanguinea', 'Alexandrium_spp',
       'Dinophysis_spp', 'Lingulodinium_polyedra', 'Prorocentrum_spp',
       'Pseudo_nitzschia_delicatissima_group',
       'Pseudo_nitzschia_seriata_group', 'Ceratium', 'Cochlodinium',
       'Gymnodinium_spp', 'Other_Diatoms', 'Other_Dinoflagellates',
       'Total_Phytoplankton']

wq_df[cols_to_float] = wq_df[cols_to_float].astype(float)

#take out the week and year info
wq_df["Sample Date"] = pd.to_datetime(wq_df["time"].str.split("T", expand=True)[0], format = '%Y-%m-%d')
wq_df["Sample Week"] = wq_df["Sample Date"].dt.isocalendar().week.astype(str)
wq_df["Sample Year"] = wq_df["Sample Date"].dt.year.astype(str)

loc_county = {'GoletaPier': 'Santa Barbara', "StearnsWharf": 'Santa Barbara', 'ScrippsPier': 'San Diego', 'SantaMonicaPier': 'Los Angeles' , 'SantaCruzWharf': 'Santa Cruz',
       'MontereyWharf': 'Monterey', 'NewportPier': 'Orange', 'CalPoly': 'San Louis Obispo'}
wq_df["County"] = wq_df["loc"].map(loc_county)

#groupby by sample year, week, location
wq_df_group = wq_df.groupby(["Sample Year", "Sample Week", "County"], as_index = False).agg("mean").reset_index()
wq_df_group.to_csv("../Data/df_WQ_grouped.csv")

