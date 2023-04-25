# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 16:05:55 2023

@author: cc743
"""

## This script processes NOAA's Community Social Vulnerability Index (CSVI) for coastal communities in CA
## The political unit for defining a community is the Census Designated Place (CDP)
## Two of the indices calculated are Fishing Reliance and Fishing Engagement
    ## And the sum of these two indices provide the overall Fishing Dependency of a CDP
    
## CDP's residing in one county have their Fishing Dependency scores averaged to represent the Fishing Dependency of a county
## Counties with higher Fishing Dependencies are considered more vulnerable to HABs because HAB-related fisheries closures are
    ## expected to have a more severe impact on communities highly dependent on fisheries resources

# Source for CSVI data taken from https://www.st.nmfs.noaa.gov/data-and-tools/social-indicators/ (filtered West Coast only)
    # Metadata found here https://www.fisheries.noaa.gov/inport/item/52041
    # Paper discussing CSVI https://repository.library.noaa.gov/view/noaa/4438
    
## Spatial data will also be attached the CSVI data using CA CDP TIGER shapefiles
    # Source of CDP and County CA data from 
    
import pandas as pd
import geopandas as gpd
import os

os.chdir("V:\\HAB_Hotspot\\Scripts") # current working directory should be the Scripts folder

csvi_dir = "..\\Data\\Raw\\NOAA_CSVI" # Get the CSVI data (downloaded)
demog_dir = "..\\Data\\Raw\\CA_demog" # Get the geometery data of counties
proc_csvi_dir = "..\\Data\\Processed\\Processed_CSVI" # Save the processed CSVI to the Processed Folder
geo_dir = "..\\Data\\Processed\\Shapefiles" # Save the shapefile
arc_dir = "..\\Data\\Processed\\For_ArcGIS" # Save clipped copy of shapefile for mapmaking

#%% Import the CSVI data, separate CDP name and County name, and calculate Fishing Dependency

csvi = pd.read_csv(os.path.join(csvi_dir, "socialIndicatorData.csv")) #[["Year", "Community Name", "State", "Latitude", "Longitude", "Commercial Engagement Categorical Ranking", "Commercial Reliance Categorical Ranking", "Recreational Engagement Categorical Ranking", "Recreational Reliance Categorical Ranking"]]
csvi = csvi.where(csvi["State"]==" CA").dropna(subset = ["Year"]) # Extract CA state
csvi["CDP"] = csvi["Community Name"].str.extract(r"(\w*\s?\w*\s?\w*)") # Extract CDP Name
csvi["COUNTY"] = csvi["Community Name"].str.extract(r"\((.*) County\)") # Extract County Info (if there are any indicated)
csvi["CDP"] = csvi["CDP"].str.upper() 
csvi["COUNTY"] = csvi["COUNTY"].str.upper() 

csvi.iloc[401, -1] = "SAN LUIS OBISPO" # BAYWOOD LOS OSOS CDP resides in SLO
csvi.iloc[420, -1]  = "CONTRA COSTA" # BAYWOOD MONTALVIN resides in Contra Costa

# Summing the commercial engagement, commercial reliance, recreational engagement, and recreational reliance represent the overall fishing dependency
    # For CA recreational engagement and reliance are unknown
csvi["Fishing Dependency Index"] = csvi["Commercial Engagement Categorical Ranking"] + csvi["Commercial Reliance Categorical Ranking"]
csvi = csvi[["Community Name", "CDP", "COUNTY", "Year", "Fishing Dependency Index"]]

#%% Use TIGER shapefiles for CDPs and Counties in CA to create a dict of CDPs and Counties (using spatial joins)

cdp_list = list( csvi["CDP"].unique() ) # Extract CDP in CSVI df

cdps = gpd.read_file(os.path.join(demog_dir, "CA_Places\\CA_Places_TIGER2016.shp")) # Import shapefile of all CA CDPs

cdps["CDP"] = cdps["NAME"].str.extract(r"(\w*\s?\w*\s?\w*)")
cdps["CDP"] = cdps["CDP"].str.upper()
cdps = cdps[["NAME", "CDP", "geometry"]] # Reduce the CDP shapefile to just CDP geometry and CDP name

cdps = cdps[cdps["CDP"].where(cdps["CDP"].isin(cdp_list)).notna()] # Reduce CDP df to only those in CSVI

counties = gpd.read_file(os.path.join(demog_dir, "CA_Counties\\CA_Counties_TIGER2016.shp")) # Import shapefile of all CA Counties
counties["COUNTY"] = counties["NAME"].str.upper() 
counties = counties[["COUNTY", "geometry"]] # Reduce County shapefile to just geometry and name

# Join the counties and cdp data based on geometry; CDPs sharing the same name but different locations are tagged with the correct County
cpds_counties_coast = cdps.sjoin(counties, how = "left", lsuffix = "_cdps", rsuffix = "_counties")

# Extract non duplicated rows and create dict of cdp and county
nonduplicates = cpds_counties_coast[~cpds_counties_coast["CDP"].duplicated(keep = False)].reset_index(0)
cpds_counties_dict = dict(zip(nonduplicates["CDP"], nonduplicates["COUNTY"]))

# Extract the duplicated rows. These are CDP's geographically in two different counties
duplicates = cpds_counties_coast[cpds_counties_coast["CDP"].duplicated(keep = False)].reset_index(0)

# Duplicate CDP's County info were verified on the political affiliation of CDPs (Google search); 
dup_dict = {"AGOURA HILLS": "LOS ANGELES", 
            "AGUANGA": "RIVERSIDE",
            "ALAMEDA": "ALAMEDA",
            "ALBANY": "ALAMEDA",
            "AMERICAN CANYON": "NAPA", 
            "ANAHEIM": "ORANGE",
            "ANTIOCH": "CONTRA COSTA",
            "AROMAS": "MONTEREY",
            "BAY POINT": "CONTRA COSTA",
            "BELL CANYON": "VENTURA",
            "BENICIA": "SOLANO",
            "BERKELEY": "ALAMEDA",
            "BLACK POINT": "MARIN",
            "BLOOMFIELD": "SONOMA",
            "BODEGA BAY": "SONOMA",
            "BREA": "ORANGE",
            "BRISBANE": "SAN MATEO",
            "BUENA PARK": "ORANGE",
            "CALABASAS": "LOS ANGELES",
            "CERRITOS": "LOS ANGELES",
            "CHINO HILLS": "SAN BERNARDINO",
            "CLAREMONT": "LOS ANGELES",
            "CYPRESS": "ORANGE",
            "DALY CITY": "SAN MATEO",
            "DIAMOND BAR": "LOS ANGELES",
            "DISCOVERY BAY": "CONTRA COSTA",
            "DUBLIN": "ALAMEDA",
            "EAST PALO ALTO": "SAN MATEO",
            "EAST WHITTIER": "LOS ANGELES",
            "EL CERRITO": "CONTRA COSTA",
            "EL SOBRANTE": "CONTRA COSTA",
            "FOSTER CITY": "SAN MATEO",
            "FREMONT": "ALAMEDA",
            "FULLERTON": "ORANGE",
            "GREENFIELD": "MONTEREY",
            "HAWAIIAN GARDENS": "LOS ANGELES",
            "HAYWARD": "ALAMEDA",
            "HERCULES": "CONTRA COSTA",
            "HIDDEN HILLS": "LOS ANGELES",
            "INTERLAKEN": "SANTA CRUZ",
            "KENSINGTON": "CONTRA COSTA",
            "LA HABRA": "ORANGE",
            "LA HABRA HEIGHTS": "LOS ANGELES",
            "LA MIRADA": "LOS ANGELES",
            "LA PALMA": "ORANGE",
            "LADERA": "ORANGE",
            "LAKEWOOD": "LOS ANGELES",
            "LAS FLORES": "ORANGE",
            "LEXINGTON HILLS": "SANTA CLARA",
            "LIVE OAK": "SUTTER",
            "LONG BEACH": "LOS ANGELES",
            "LOS ALAMITOS": "ORANGE",
            "LOS ANGELES": "LOS ANGELES",
            "MARTINEZ": "CONTRA COSTA",
            "MENLO PARK": "SAN MATEO",
            "MILPITAS": "SANTA CLARA",
            "MONTCLAIR": "SAN BERNARDINO",
            "MOUNTAIN HOUSE": "SAN JOAQUIN",
            "NORRIS CANYON": "CONTRA COSTA",
            "OAK PARK": "VENTURA",
            "OAKLAND": "ALAMEDA",
            "PAJARO": "MONTEREY",
            "PAJARO DUNES": "SANTA CRUZ",
            "PALO ALTO": "SANTA CLARA",
            "PINOLE": "CONTRA COSTA",
            "PITTSBURG": "CONTRA COSTA",
            "POMONA": "LOS ANGELES",
            "PORTOLA VALLEY": "SAN MATEO",
            "PRUNEDALE": "MONTEREY",
            "RAINBOW": "SAN DIEGO",
            "REDWOOD CITY": "SAN MATEO", 
            "RICHMOND": "CONTRA COSTA",
            "RIO VISTA": "SOLANO",
            "ROLLING HILLS": "LOS ANGELES",
            "ROSAMOND": "KERN",
            "ROWLAND HEIGHTS": "LOS ANGELES",
            "SAN CLEMENTE": "ORANGE",
            "SAN FRANCISCO": "SAN FRANCISCO",
            "SAN JOSE": "SANTA CLARA",
            "SAN RAFAEL": "MARIN",
            "SAN RAMON": "CONTRA COSTA",
            "SANTA MARIA": "SANTA BARBARA",
            "SEA RANCH": "SONOMA",
            "SEAL BEACH": "ORANGE",
            "SIMI VALLEY": "VENTURA",
            "SOUTH SAN FRANCISCO": "SAN MATEO",
            "SPRING VALLEY": "SAN DIEGO",
            "STANFORD": "SANTA CLARA",
            "STRAWBERRY": "MARIN",
            "SUNNYVALE": "SANTA CLARA",
            "TEMECULA": "RIVERSIDE",
            "THOUSAND OAKS": "VENTURA",
            "TIBURON": "MARIN",
            "UPLAND": "SAN BERNARDINO",
            "VALLEJO": "SOLANO",
            "VALLEY FORD": "SONOMA",
            "WATSONVILLE": "SANTA CRUZ",
            "WESTLAKE VILLAGE": "LOS ANGELES",
            "WHITTIER": "LOS ANGELES",
            "WILLOW CREEK": "HUMBOLDT",
            "WINTERS": "YOLO",
            "YORBA LINDA": "ORANGE",
            "MOUNTAIN VIEW CITY": "SANTA CLARA",
            "BURBANK CITY": "LOS ANGELES",
            "BURBANK CDP": "SANTA CLARA",
            "MOUNTAIN VIEW CDP": "SANTA CLARA",
            "EAST LA MIRADA": "LOS ANGELES",
            "SEVEN TREES": "SAN JOSE",
            "CRESCENT CITY NORTH": "DEL NORTE",
            "WALDON": "CONTRA COSTA",
            "EAST COMPTON": "LOS ANGELES",
            "WEST COMPTON": "LOS ANGELES",
            "OPAL CLIFFS": "SANTA CRUZ",
            "SUNSET BEACH": "ORANGE",
            "JURUPA VALLEY": "RIVERSIDE"
            }

cpds_counties_dict.update(dup_dict)# complete dict of cdp and counties

#%% Fill in the missing County data in the CSVI df and aggregate the Fishing Dependencies of CDPS by County and Year of CSVI assessment

csvi["COUNTY"] = csvi["COUNTY"].fillna(csvi["CDP"].map(cpds_counties_dict))
csvi_county = csvi.groupby(["COUNTY", "Year"]).agg(["sum", "mean", "median", "max", "min", "count"]).reset_index() # see that Fishing Dependency overall does not change a lot over tie

# Save this summary of Fishing Dependencies of County across time
csvi_county.to_csv(os.path.join(proc_csvi_dir, "csvi_county_summary.csv"))

#%% Subset the 2019 CSVI data and add spatial info

# Edit the CSVI data by dropping levels and selecting only 2019 Year
csvi_county.columns = csvi_county.columns.droplevel()
csvi_county = csvi_county.set_axis(['COUNTY', 'Year', 'FDI Sum', 'FDI Mean', 'FDI Median', "FDI Max", "FDI Min", "# CDPs"], axis=1, inplace=False)
csvi_2019 = csvi_county.where(csvi_county["Year"] == 2019).dropna().drop(columns = "Year")
csvi_2019.to_csv(os.path.join(proc_csvi_dir, "county_CSVI_2019.csv")) # save this summary of just 2019 CSVI data

# Add spatial info
csvi_2019 = gpd.GeoDataFrame(csvi_2019.merge(counties, left_on="COUNTY", right_on="COUNTY"), crs ="EPSG:3857", geometry = "geometry")
csvi_2019.to_file(os.path.join(geo_dir, "county_CSVI_2019.shp"))

#%% Clip the CSVI shapefile to CA boundary

import arcpy 
import os

# Arc Set up
arcpy.env.workspace = arc_dir
arcpy.env.extent = "-127.499997461121 32.5342903 -114.999994909484 42.000000772404"
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("WGS 1984")

# Clip using online Feature Layer by Brian Shaw
mask = "https://services2.arcgis.com/C8EMgrsFcRFL6LrL/arcgis/rest/services/US_States_and_Territories/FeatureServer/0"
da_clip = arcpy.analysis.Clip(os.path.join(geo_dir, "county_CSVI_2019.shp"), mask)