# -*- coding: utf-8 -*-
"""                                                        
Created on Tue Feb 21 15:50:49 2023

@author: cc743
"""

## This script accesses the Domoic Acid sampling data collected by 
    ## California Department of Public Health (CDPH) between 2000-2021
    ## for multiple species (various crab, mussels, clam, and anchvies)
## The data is spread across four excel sheets and were combined into one larger
    ## .csv file 
## https://github.com/cfree14/domoic_acid_mgmt (Chris Free's GitHub link, 
    ## this GitHub contains the Domoic Acid sampling data for CA, OR, WA)
    
import pandas as pd
import os

os.chdir("V:\\HAB_Hotspot\\Scripts") # current working directory should be the Scripts folder

# Raw Domoic Acid sampling data stored in Raw directory and processed
    # version will be stored in the Processed directory
    
raw_da_dir = "..\\Data\\Raw\\Free_et_al_Data\\sample_data"
proc_da_dir = "..\\Data\\Processed\\Processed_DA"

#%% Import the raw data (three .csvs; 2000-2021) 

#crab meat data from 2000 to 2016
df1 = pd.read_excel(os.path.join(raw_da_dir,"CDPH_DA_2000_crab.xlsx"))

#non crab meat data from 2000 to 2013
df2 = pd.read_excel(os.path.join(raw_da_dir,"CDPH_DA_2000-2013.xls.xlsx"))

#non crab meat data 2014 to 2021
df3 = pd.read_excel(os.path.join(raw_da_dir,"DA_2014-2021_CDPH_061121.xls.xlsx"), sheet_name = "DA_2014-2021_CDPH_n_061121")

#%% Import the raw data (one xls; summer 2021)
    # this data different columns and data schema
    # wrangle this to concat with the other dfs smoothly
    
df4 = pd.read_csv(os.path.join(raw_da_dir,"CrabDAWebResultsJuly12021toNovember242021.csv")).reset_index()

# pivot table so each individual samples is represented by a row, 
    # assume the one nan value is a "<2.5"
df4_long = pd.wide_to_long(df4, stubnames = "sample", i = "index", j = "type1").reset_index().drop(columns = ["index", "type1", "da_ppm_avg", "percent_over"]).fillna("<2.5")

# add county data for the sampling sites (to observe DA events by county area)

df4_long["Sample Site"] = df4_long["site"] + ", " + df4_long["port"]
df4_long["ASP -ug/g-"] = df4_long["sample"].str.extract(r"(\d.*\d*)") #some DA sampels had "non-detect" or below 2.5 or 1 ppm. can ignore this because 2.5 and 1 are below the thresholds for 20 and 30 ppm (since we're interested in DA events not concentrations)
df4_long["Mod-ASP"] = df4_long["sample"].str.extract(r"(<)")
df4_long["ASP -ug/g-"] = df4_long["ASP -ug/g-"].astype(float)
df4_long["Sample Type"] = df4_long["type"]
df4_long["Date -Sampled-"] = pd.to_datetime(df4_long["date"])
df4_long = df4_long.drop(columns = ["type", "site", "port" , "date", "sample"])

#%% Concat the data and save the csv to the Processed Folder

df_DA = pd.concat([df1,df2,df3,df4_long]).drop(columns = ["SRL #", "# of individuals", "Notes"]).rename(columns = {"area": "Zone"})
df_DA = df_DA.reset_index(drop = True)
df_DA = df_DA[df_DA["Sample Type"].str.contains("Dungeness")] # select only Dungeness Crab; assume NANs are not crab

df_DA.to_csv(os.path.join(proc_da_dir,"df_DA_samples_DC.csv")) #combine raw data (still needs more processing to fill NaN vals for sampling locations)

