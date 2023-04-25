Creator: Curtis Cha
Date: 03/28/2023

Title: Identifying Algal Bloom Hotspots, areas with high Domoic Acid Event frequency, and fishing dependent communities

-------------------------------------------

Background

Biotoxins produced by HABs pose a significant public health risk, prevent fishing livelihoods, 
and disrupt social and cultural ties to the fishery resource. On the West Coast, Pseudo-nitzschia spp. 
is one algal group that produces the neurotoxin, Domoic Acid (Free et al). During blooms of Pseudo-nitzschia, 
Domoic Acid can contaminate shellfish and bioaccumulate higher up the food chain (Free). When consumed, 
Domoic Acid causes Amnesic Shellfish Poisoning and symptoms range from gastrointestinal distress to fatal 
neurological disorders (Free et al). In the interest of public health, West Coast states regularly monitor 
shellfish samples for biotoxin contamination (Free et al). Domoic Acid events occur when Domoic Acid levels 
exceed a regulatory threshold of 20 ppm for shellfish and crab meat and 30 ppm for crab viscera. 
In response to a Domoic Acid event, states must take management action for the contaminated fishery resource (Free et al, Stuchal et al 2020, doi: 10.1016/j.yrtph.2020.104759). If changing ocean conditions increase the frequency and severity of HABs on the West Coast, then Domoic Acid events are also likely to increase in frequency. 

The objective of this project was to apply my skills in ArcGIS Pro, Python, and data management. 
Since the previous projects surround the topic of Harmful Algal Blooms, I decided to identify algal 
bloom hotspots, or areas of high algal productivity, off the West Coast using satellite-imagery
Chlorophyll-a data from 2005-2020. I also analyzed Domoic Acid monitoring data to examine where Domoic
Acid events frequently occur. HAB-related fisheries closures can have significant impacts on communities 
dependent on fishing for livelihood. I also wanted to examine where vulnerable communities are located 
in relation to algal bloom hotspots and Domoic Acid events. To determine “vulnerability”, I relied on NOAA’s 
Community Social Vulnerability Index (CSVI) for coastal communities. 

-------------------------------------------

Methods:

This project uses satellite imagery data, shellfish monitoring data, and NOAA’s 2019 Community Social 
Vulnerability Index (CSVI) data for the state of California. Satellite imagery of surface water Chlorophyll-a 
was collected from the MODIS-AQUA satellite and accessed through NOAA Coast Watch’s ERDDAP service. 
The data represents weekly average Chlorophyll-a concentrations (micrograms/L) between 2005 and 2020. Chlorophyll-a is an 
indicator of phytoplankton biomass and water concentrations of 25-40 micrograms/L are considered “at-risk” 
(Sutula et al 2017). While satellite imagery allows for quicker examination of phytoplankton production 
over a larger area, it is restricted to only production at surface waters. For this project, surface water 
Chlorophyll-a are assumed to be representative of phytoplankton productivity of the water column. To represent 
an “algal bloom week”, areas with weekly average concentrations greater than ____mg/L were assigned a value of 1. 

Total number of algal bloom weeks were calculated for between 2005 and 2020 and hotspots are represented by areas 
with higher total algal bloom weeks . Domoic Acid monitoring data represents Domoic Acid concentrations in shellfish 
and fish samples over time for monitoring stations in CA and accessed through Chris Free’s GitHub. If a sample 
exceeded regulatory thresholds, then the sample was assigned a value of 1 to represent a “Domoic Acid event”. 
To match the weekly interval of the Chlorophyll-a data, weeks that observed at least one Domoic Acid event were 
assigned a value 1 to represent “Domoic Acid Event Week”. Between the years 2005 and 2020, the number of Domoic Acid 
Event Weeks observed was summed by county to show where the most Domoic Acid Events have occurred.

CSVI are a collection of indices calculated for coastal communities based on US census data, NOAA and states fisheres
data. The CSVI data is calculated every year between 2009-2019 and accessed through NOAA’s Office of Science 
and Technology (https://www.st.nmfs.noaa.gov/data-and-tools/social-indicators/). “Fishing Dependency” scores can be
calculated by summing two indices of the CSVI: Fishing Reliance and Fishing Engagement (Jepson & Colburn 2013). 
The most recent CSVI data comes from the 2019 US Census and the indices for Fishing have remained relatively unchanged. 
The political unit for CSVI is the “Census-Designated Place” (CDP). To share the same spatial scale as the Domoic Acid data, 
mean Fishing Dependency scores were calculated across CDP’s within the same county. While this statistic does remove the 
variability of Fishing Dependency Scores between CDPs within a county, it allows for easier comparison with the 
Domoic Acid event data. However, some counties are represented by only a few CDPs. Certain calculated 
Fishing Dependencies may not truly represent the fishing community vulnerability of counties because not enough CDPs
are represented in the data. Counties with higher Fishing Dependency scores represent vulnerable communities as they are 
likely to be more severely impacted by HAB-related fisheries closures than counties with lower Fishing Dependency 
scores.

-------------------------------------------

Data Sources

- MODIS-AQUA Satellite Imagery (Weekly Mean Chlorophyll-a Data (mg/m3) and 8-day Mean Sea Surface Temperature (deg C)), 4km
    
  Data Source: https://coastwatch.pfeg.noaa.gov/erddap/griddap/erdMH1chla8day.html
  
  Data Information: Satellite Imagery collected by NASA's MODIS AQUA for Chlorophyll-a and SST.
    (metadata: https://coastwatch.pfeg.noaa.gov/erddap/info/erdMH1chla8day_R2022NRT/index.html)

- Domoic Acid Monitoring Data: Domoic Acid concentrations (ppm) of shellfish and fish samples in CA 

  Source: https://github.com/cfree14/domoic_acid_mgmt   *** only OR and CA data is for public use, WA data requires permission from MERHAB
  
  Data Information: Monitoring data is collected by state health departments. When concentrations exceed a regulatory
  threshold of 20ppm, fisheries management action must be taken. This may result in the delay or closures of the
  relevant fisheries to protect seafood consumers. Dr. Chris Free used this data for a research paper analyzing 
  Domoic Acid management in the West Coast. 
  
  Research Paper: Free CM, Moore SK, Trainer VL (2022) The value of monitoring in efficiently and adaptively managing biotoxin contamination in marine fisheries. Harmful Algae 114: 102226.
    (https://www.sciencedirect.com/science/article/pii/S1568988322000543?dgcid=author)
    
- NOAA CSVI: Community Social Vulnerability Index (14 Indices) calculated by NOAA based on US Census Data and
  Commercial & Recreational Fisheries data
 
  Source: https://www.st.nmfs.noaa.gov/data-and-tools/social-indicators/

  Data Information: "The NOAA Fisheries Community Social Vulnerability Indicators (CSVIs) data series from 2009 to 2018 
  is comprised of a suite of indicators that describe and evaluate a coastal community’s ability to respond to 
  changing social, economic and environmental conditions...The 14 indices measure facets of commercial and recreational 
  fishing dependence, social and gentrification pressure vulnerability and climate change vulnerability. The indices enable 
  the comparison of these conditions for over 4,600 coastal communities in 23 states. The indicators illustrate geographic 
  and temporal variation in these conditions. The social indicators were developed with multiple sources of data. Data are 
  primarily drawn from the United States Census Bureau’s American Community Survey 5-year estimates and NOAA Fisheries. The 
  social and gentrification pressure vulnerability indices were calculated with U.S. Census American Community Survey (ACS) 
  five year rolling average estimate data from 2005-2009 to 2014-2018. The commercial fisheries indicators were developed 
  using NOAA Fisheries landings data from 2009 to 2018. The recreational fisheries indicators were developed from 2009 to 
  2018 with NOAA fisheries and/or state (Texas, Louisiana, California, Oregon, Washington and Alaska) data unique to each 
  region." - quoted from Abstract in Source Link
  
    (metadata: https://www.fisheries.noaa.gov/inport/item/52041)
  
  Research Paper: Jepson, Michael and Lisa L. Colburn 2013. Development of Social Indicators of Fishing Community Vulnerability and Resilience in the U.S. Southeast and Northeast Regions. U.S. Dept. of Commerce., NOAA Technical Memorandum NMFS-F/SPO-129, 64 p.
    (https://repository.library.noaa.gov/view/noaa/4438)

- CA Demography: TIGER Shapefiles for Census-Designated Places, Counties, and State Boundaries of California

  Source: https://data.ca.gov/dataset/ca-geographic-boundaries
  
  Data Information: "This dataset contains shapefile boundaries for CA State, counties and places from the US Census 
  Bureau's 2016 MAF/TIGER database. The 2016 TIGER/Line Shapefiles contain current geography for the United States, the 
  District of Columbia, Puerto Rico, and the Island areas. Current geography in the 2016 TIGER/Line Shapefiles generally 
  reflects the boundaries of governmental units in effect as of January 1, 2016, and other legal and statistical area 
  boundaries that have been adjusted and/or corrected since the 2010 Census. This vintage includes boundaries of governmental 
  units that match the data from the surveys that use 2016 geography, such as the 2016 Population Estimates and the 2016 
  American Community Survey. The 2016 TIGER/Line Shapefiles contain the geographic extent and boundaries of both legal and 
  statistical entities. A legal entity is a geographic entity whose boundaries, name, origin, and area description result 
  from charters, laws, treaties, or other administrative or governmental action. A statistical entity is any geographic 
  entity or combination of entities identified and defined solely for the tabulation and presentation of data. Statistical 
  entity boundaries are not legally defined and the entities have no governmental standing." - quoted from Abstract in Source Link
  
    Metadata: same as Source

- Land Mask:  ArcGIS Online Feature Layer by Brian Shaw "US States and Territories"

  Source: https://services2.arcgis.com/C8EMgrsFcRFL6LrL/arcgis/rest/services/US_States_and_Territories/FeatureServer
-------------------------------------------
Tools:

Python to manage the various data sets:
 --> Libraries used: os, pandas, geopandas, xarray, arcpy
 
ArcGIS Pro to produce map products
 --> Import the two shapefiles and TIF in the "For-ArcGIS" folder into ArcGIS Pro   
-------------------------------------------

Directories

1. Data - This directory holds both the raw and processed data for this project

2. Scripts - This data holds the scripts that wrangle and process the data for this project
3. Docs - This data holds the PDF's of the maps produced by ArcGIS
