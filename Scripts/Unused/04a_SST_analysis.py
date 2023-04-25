# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 13:58:41 2023

@author: cc743
"""


import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
#  as of 2022-12-26: max date range for chlor_a is 2003-01-05 to 2022-03-26 and max date range for sst is 2002-07-04 to 2022-03-30

# point data from Chris Free is available for OR and CA only, this data will subset to CA
sst = xr.open_dataset("..\\Data\\Raw\\MODIS_AQUA\\sst_raw.nc")

# subset into seasons
def jfm(month) :
        return (month >= 1) & (month <= 3)
def amj(month) :
    return (month >= 4) & (month <= 6)
def jas(month) :
    return (month >= 7) & (month <= 9)
def onb(month) :
    return (month >= 10) & (month <= 12)

raw_dir = "..\\Data\\Raw\\MODIS_AQUA"
proc_dir = "..\\Data\\Processed"

#%% SST 20 year
#create single data array of the 20 year avg for SST, and seasonal
sst_2003 = sst.sel(time = slice("2003-01-01","2003-12-31")).sst
sst_mean = sst_2003.mean("time")

# sst = sst.assign(diff_C = sst.sst - sst_mean.data) sst_mean.data could be replaced with a "proxy" SST value (mean of previous five years) to assess SST anomaly
sst.to_netcdf(os.path.join(proc_dir, "sst_proc.nc"))

sst.diff_C.mean("time").where(sst.mask == 2).plot()

# subset into seasons; to find should use the difference between the seasonal average
winter_sst = sst.sel(time = jfm(sst["time.month"]))
winter_mean = sst_2003.sel(time = jfm(sst_2003["time.month"])).mean("time")
winter_sst = winter_sst.assign(diff_C_szn = winter_sst.sst - winter_mean.data)
winter_sst.to_netcdf(os.path.join(proc_dir,"sst_winter.nc"))

spring_sst = sst.sel(time = amj(sst["time.month"]))
spring_mean = sst_2003.sel(time = amj(sst_2003["time.month"])).mean("time")
spring_sst = spring_sst.assign(diff_C_szn = spring_sst.sst - spring_mean.data)
spring_sst.to_netcdf(os.path.join(proc_dir, "sst_spring.nc"))

summer_sst = sst.sel(time = jas(sst["time.month"]))
summer_mean = sst_2003.sel(time = jas(sst_2003["time.month"])).mean("time")
summer_sst = summer_sst.assign(diff_C_szn = summer_sst.sst - summer_mean.data)
summer_sst.to_netcdf(os.path.join(proc_dir,"sst_summer.nc"))

fall_sst = sst.sel(time = onb(sst["time.month"])) 
fall_mean = sst_2003.sel(time = onb(sst_2003["time.month"])).mean("time")
fall_sst = fall_sst.assign(diff_C_szn = spring_sst.sst - spring_mean.data)
fall_sst.to_netcdf(os.path.join(proc_dir,"sst_fall.nc"))

spring_sst.diff_C.mean("time").where(spring_sst.mask ==2).plot(cmap = "plasma")
summer_sst.diff_C.mean("time").where(summer_sst.mask ==2).plot(cmap = "plasma")
fall_sst.diff_C.mean("time").where(fall_sst.mask ==2).plot(cmap = "plasma")
winter_sst.diff_C.mean("time").where(winter_sst.mask ==2).plot(cmap = "plasma")

