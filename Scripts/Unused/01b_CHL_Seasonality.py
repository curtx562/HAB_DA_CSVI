# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 11:58:13 2023

@author: cc743
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 00:45:40 2022

@author: cc743
"""
import rioxarray
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

#  as of 2022-12-26: max date range for chlor_a is 2003-01-05 to 2022-03-26, select date range 2005-2020)

proc_dir = "..\\Data\\Processed"
unused_dir = "..\\Data\\Processed\\Unused"
#%% CHL 20 year

bloom = xr.open_dataset(os.path.join(proc_dir, "bloom_proc.nc"))

# subset into seasons
def jfm(month) :
    return (month >= 1) & (month <= 3)
def amj(month) :
    return (month >= 4) & (month <= 6)
def jas(month) :
    return (month >= 7) & (month <= 9)
def onb(month) :
    return (month >= 10) & (month <= 12)

# seasons; McCabe mentions the upwelling season as AMJ and compares to the winter months JFM
winter_bloom = bloom.sel(time = jfm(bloom["time.month"]))
winter_bloom.to_netcdf(os.path.join(unused_dir, "chl_winter.nc"))
spring_bloom = bloom.sel(time = amj(bloom["time.month"]))
spring_bloom.to_netcdf(os.path.join(unused_dir, "chl_spring.nc"))
summer_bloom = bloom.sel(time = jas(bloom["time.month"]))   
summer_bloom.to_netcdf(os.path.join(unused_dir, "chl_summer.nc"))
fall_bloom = bloom.sel(time = onb(bloom["time.month"]))   
fall_bloom.to_netcdf(os.path.join(unused_dir, "chl_fall.nc"))

winter_mean = winter_bloom.bloom.mean("time")#.where(winter_bloom.mask ==2)#.plot()
winter_mean.to_netcdf(os.path.join(unused_dir, "bloom_winter_mean.nc"))
spring_mean = spring_bloom.bloom.mean("time")#.where(spring_bloom.mask ==2)#.plot()
spring_mean.to_netcdf(os.path.join(unused_dir, "bloom_spring_mean.nc"))
summer_mean = summer_bloom.bloom.mean("time")#.where(summer_bloom.mask ==2)#.plot()
summer_mean.to_netcdf(os.path.join(unused_dir, "bloom_summer_mean.nc"))
fall_mean = fall_bloom.bloom.mean("time")#.where(fall_bloom.mask ==2)#.plot()
fall_mean.to_netcdf(os.path.join(unused_dir, "bloom_fall_mean.nc"))