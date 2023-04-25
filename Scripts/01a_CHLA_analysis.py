# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 00:45:40 2022

@author: cc743
"""

## This script accesses ERDDAP from NOAA Coast Watch 
## for MODIS CHLA (in milligrams/cubic metere or microgram/L)
## and downloads the data as a netcdf

# https://coastwatch.noaa.gov/cwn/index.html (Home Page for NOAA Coast Watch)
# https://coastwatch.pfeg.noaa.gov/erddap/search/index.html?page=1&itemsPerPage=1000&searchFor=chlorophylla (Catalog of Datasets)

import xarray as xr
import os

os.chdir("V:\\HAB_Hotspot\\Scripts") # current working directory should be the Scripts folder

# Raw data will be stored in the Raw Folder, Processed data in Processed Folder
raw_dir = "..\\Data\\Raw\\MODIS_AQUA"
proc_nc_dir = "..\\Data\\Processed\\Processed_nc"
arc_dir = "..\\Data\\Processed\\For_ArcGIS" # Save files for mapmaking

#%% Download the NetCDF from OpenDAP/THREDDS and create NetCDFs

# use weekly chlor_a data to avoid the issues of NA in the daily data; significant HAB events (i.e. Red Tides in FL) last on the scale of weeks to months
chlor_a_raw = xr.open_dataset("https://coastwatch.pfeg.noaa.gov/erddap/griddap/erdMH1chla8day")

# reduce area coverage and specify date range (2005-2020) to reduce the size of data downloaded
chl_sub = chlor_a_raw.sel(latitude = slice(42,32), longitude = slice(-127.5, -115), time = slice("2005-01-01", "2020-12-31")) 

#chl_sub.to_netcdf(os.path.join(raw_dir, "chlor_raw.nc")) # may be useful to save raw data at this step, servers may be down / connection off
#%% Add data to represent "bloom" events and save the new file
## Create data array that assigns "bloom" value for each pixel for a given time
## Picking a threshold: 
    ## Sutula et. al. suggest 24-40 mg/m&3 as an "at-risk" threshold
    ## doi:10.1016/j.ecss.2017.07.009

bloom = xr.where(chl_sub.chlorophyll > 35, 1, 0)
chl_sub["bloom"] = bloom
## Selecting a statistic to represent the time range
    ## 'med' returns only one value, because bloom values are "infrequent" 
    ## 'mean' and 'total sum' show similar results, as the max value for
        ## 'mean' is actually percentage of sample weeks that observed an algal bloom 
        ## because bloom is county data
        
bloom_mean = chl_sub.bloom.mean(dim = "time")#.where(chlor_a_2.mask == 2)#.plot()
#bloom_sum = bloom.sum(dim ='time')
#bloom_count = bloom.count(dim = 'time')

bloom_mean.plot() # ## QAQC to check if code produces a correct raster (instead of single-value raster)

#%% Save the data as a .tif

import rioxarray

bloom = os.path.join(proc_nc_dir, "bloom_mean.tif")
bloom_mean.rio.to_raster(bloom, driver="COG")
#bloom_mean.to_netcdf(os.path.join(proc_nc_dir, "bloom_mean.nc"))

#%% Clip the .tif to match CA boundary

import arcpy 
import os

# Arc Set up
arcpy.env.workspace = arc_dir
arcpy.env.extent = "-127.499997461121 32.5342903 -114.999994909484 42.000000772404"
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("WGS 1984")

# Clip using online Feature Layer by Brian Shaw
mask = "https://services2.arcgis.com/C8EMgrsFcRFL6LrL/arcgis/rest/services/US_States_and_Territories/FeatureServer/0"
bloom_clip = arcpy.sa.ExtractByMask(bloom, mask, "OUTSIDE")
bloom_clip.save(os.path.join(arc_dir, "bloom_mean.tif"))
