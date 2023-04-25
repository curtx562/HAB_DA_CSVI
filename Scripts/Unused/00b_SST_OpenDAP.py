# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 11:55:37 2023

@author: cc743
"""

import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

data_dir = "..\\Data\\Raw\\MODIS_AQUA"

#%% Download the NetCDF from OpenDAP/THREDDS and create NetCDFs
## OpenDAP/THREDDS from JPL for MODIS SST
## https://thredds.jpl.nasa.gov/thredds/catalog.html ##this link not working and Aqua MODIS Global Daytime 8day from NOAA Coast Wath also not working

## OpenDAP/THREDDS from NOAA Coast Watch for MODIS CHLA (in milligrams/cubic metere or microgram/L)
## https://oceanview.pfeg.noaa.gov/projects
## https://oceanwatch.pfeg.noaa.gov/thredds/catalog/catalog.html
# use weekly chlor_a data to avoid the issues of NA in the daily data; significant HAB events (i.e. Red Tides in FL) last on the scale of weeks to months


sst_raw = xr.open_dataset("https://thredds.jpl.nasa.gov/thredds/dodsC/ncml_aggregation/OceanTemperature/modis/aqua/11um/4km/aggregate__MODIS_AQUA_L3_SST_THERMAL_8DAY_4KM_DAYTIME_V2019.0.ncml")

sst_sub = sst_raw.sel(lat = slice(42,32), lon = slice(-127.5, -115))

#%% set up the mask

# masking in the xarry, ocean areas are assigned 2 while land are assigned 1
mask_ocean = 2 * np.ones((sst_sub.dims['lat'], sst_sub.dims['lon'])) * np.isfinite(sst_sub.sst.isel(time = 0))  
mask_land = 1 * np.ones((sst_sub.dims['lat'], sst_sub.dims['lon'])) * np.isnan(sst_sub.sst.isel(time = 0))
mask_array = mask_ocean + mask_land
sst_sub.coords['mask'] = (("lat", "lon"), mask_array.data)
chl_sub.coords['mask'] = (("lat", "lon"), mask_array.data)
#arcgis; mask out land areas and lake areas; reduce to shorter dist off shore


#%%save the NetCDF

sst_name = "sst_raw.nc"

sst_sub.to_netcdf(os.path.join(data_dir, sst_name)) 
