This README describes the Python scripts within this directory.
Script Prefixes indicate the "order" of running starting at "00a_" and ending at "03_"

Scripts:

- 01a_CHLA_analysis: 
  
    This script accesses and downloades the NetCDF files for MODIS-AQUA's weekly mean Chlorophyll-a data (2004-2022) for 
    the ocean areas off CA through NOAA Coast Watch ERDDAP. 
    
    This script processes the NetCDF of Chlorophyll-a data to add a binary value to areas with greater than
    35 mg/m^3 Chlorophyll-a. These values represent weeks that observed an "algal bloom" event in a given area.
    
    The NetCDF was "flattened" across time to produce a raster that calculates the percentage of 
    weeks between 2005-2020 that observed an algal bloom event. This raster was used in ArcGIS Pro
    to make the map product.
    
    ** There is one week "not sampled" between 12-29 to 01-05

- 02a_DA_data_combine:
    
     This script accesses the Domoic Acid monitoring data which contains information about shellfish samples between 2000-2021.
     The data is split across four CSV files and these four were combined to produce a single CSV with all shellfish samples and 
     the Domoic Acid concentrations.
     
     ** Should produce a graph that shows the number of samples taken across time (see if there's a pattern in sampling times)
   
- 02b_DA_data_sites:
  
    This script continues to process the Domoic Acid monitoring data by filling in missing coordinate, county, fisheries management zone
    data of samples. A dictionary was created to collect existing data about sampling sites and coordinate data. For some samples, coordinate
    data was already collected in other samples that share the sampling site. However, sampling sites that no coordinate data
    throughout the CSV had to be manually researched. This will introduce some error into the data because coordinate points found
    through Google Maps reflect the general location of the sample site, not the specific location of the sample itself. This method 
    was repeated to collect County data of samples. When researching County information of sample sites, Google was also used to find
    link sample sites to counties based on political boundaries.  For Management Zones, a for loop was used to classify samples based on 
    their latitudes. The final dict was used to fill in the missing location data of samples and save an updated version of the CSV
    of Domoic Acid monitoring data.
    
    ** Geopandas can be utilized to link sample sites to counties using spatial join, but this ignores political boundaries (yields
    different results from the manual research method.
    ** May want to focus just on Dungeness Crab samples because the 20ppm threshold is assumed for other shellfish (and some fish samples)
    
- 02c_DA_process_zone:
    
    This script is the next processing step of the Domoic Acid monitoring data. It separates the Sampling Date column into numeric
    Year, Month, Week columns. Then, it adds a column representing "Domoic Acid Event" with a binary based on the Domoic Acid concentrations
    of the sample. For concentrations greater than 20ppm, a value of 1 was assigned to the "Domoic Acid Event" column. However, if the
    sample was of viscera meat from Dungeness Crab, then management action is only need for greater than 30ppm. The CSV was then subset
    to only the samples collected between 2005-2020 to match the time frame of the Chlorophyll-a data set. The data was then grouped
    by Management Zone and Sample Week/Year and a new column "Domoic Acid Week" was added. If a Zone during a given week observed at least 
    one Domoic Acid, the "Domoic Acid Week" was assigned a value of 1. This was to create a data column that matches the weekly mean 
    Chlorophyll-a satellite imagery data. 
    
    Based on the latitude of the management zone boundaries in Free et al., the state of CA TIGER shapefile was split into the eight management 
    zones (A to H). The final data aggregates total "Domoic Acid Weeks" observed for each zone, and zone spatial data was added. This was then 
    saved as shapefile and used in ArcGIS Pro to produce map products.
   
- 03_CSVI: 

    This script processes NOAA's CSVI for fishing communities in the United States between 2009-2019. The raw CSV was subset to only 
    include the state of CA. Fisheries indices are calculated based on fishing landings data and relevant NOAA or state-specific
    recreational fishing data. The indices of this data represent "Census-Designated Place" which is identified by the US Census Bureau. 
    For each CDP, the "Fishing Dependency" Index was calculated by summing Fishing Reliance and Fishing Engagement for commercial and 
    recreational fishing (Colburn). However, the state of CA has no indices for recreational fishing so Fishing Dependency is calculated 
    only based on commercial fishing activity. A new column was added to represent "County" data for CDP's and, for some CDPs, 
    the County information was indicated in the CDP name. CDP location data was also added to the CSV using the TIGER shapefile for CA
    CDPS. Using the spatial join function in geopandas with the TIGER shapefile for CA Counties, County data was filled in for CDPs.
    This function duplicated rows for CDPs that were geographically shared between two counties, CDPs that 
    shared names. Non-duplicated CDPs were extracted to a dictionary item with their County information. Duplicated CDPs had to be 
    researched on Google to find out their County based on political affiliation. The County information for duplicated CDPs was 
    added to the dictionary of CDPs and COunties, then this dictionary was used to fill in missing County data. Then, this data was
    aggregated by County and Year to calculated total, mean, median, maximum, minimum, and standard deviation of the Fishing Dependency 
    values of CDPs within the county. The statistics suggest that Fishing Dependency does not change much over time so the data was subset
    to the most recent year 2019. Geospatial data for counties was added to the 2019 Fishing Dependency Data for CA Counties, saved as a shapefile, 
    and used in ArcGIS Pro to produce map products.
    
------------------------------------

For the UNUSED Directory, this contains scripts that are incomplete or produced products that are currenlty not in use

- 00b_SST_OpenDAP:
  
    This script accesses and downloads the NetCDF files for MODIS-AQUA's weekly mean Sea Surface Temperatures for CA waters (2003-2021)
   ** Link is to NOAA CoastWatch OpenDAP and may not work. ERDDAP link may work
    
- 01b_CHL_Seasonality:
  
    This script separates the Chlorophyll-a NetcDF file by season and produces mean bloom rasters for each season. Visually, there seems to be
    significant differnces between algal productivity by seasons.
    
- 02d_DA_data_process_zone:

    This script aggregates Domoic Acid Event and Weekly Domoic Acid Event data into Counties.
    
- 02e_Time_Series_DA:
  
    This script adds "non-sample" Sample Week-Years by County to the Domoic Acid monitoring data aggregated by County and Sample Week-Year. Non-sample
    weeks are assumed to have 0 Domoic Acid events. This was made to possibly explore with time-series tools.
    
- 04a_SST_analysis:

    This script separates the SST NetcDF file by season and produces mean SST for each season. Visually, there seems to be
    significant differnces between SST by seasons. It does not include code for subtracting SST mean of a previous time period to calculate
    SST anomaly.
    
- 05_WQ_data:

    This script uses Water Quality monitoring data taken from an older project completed Spring 2023 (https://github.com/curtx562/Cha_OBrien_ENV872_EDA_FinalProject/tree/main/Data/Raw)/
    Data is originally taken from California's HAB monitoring system (CalHABMAP: https://calhabmap.org/about-us). It collects water sample data taken 
    from CA and records the various algal species, algal biotoxins, SST, and nutrient concentrations. This was significant because it monitors both
    Domoic Acid concentrations in water and the presence the Pseudonitzschia spp. (the producer of Domoic Acid). However, the data is not sampled
    regularly and Northern CA water samples begin in 2019. (OUTDATED CODE, WILL RUN INTO ERRORS). ** Previous project already processed this data and ran some 
    time series analysis on it. 