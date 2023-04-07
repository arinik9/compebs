'''
Created on Nov 29, 2022

@author: nejat
'''


import os
import pandas as pd
import numpy as np
import datetime
import json
import copy
import math
from PAMI.partialPeriodicSpatialPattern.basic import STEclat

from util_gis import haversine




# calculate the neighborhood by distance
def get_zone_neighbors(df_spatial_entity_info, tresh_distance_in_km):
    spatial_entity_list = []
    
    for index, row in df_spatial_entity_info.iterrows():
      geonameId = row["geonameId"] # geonames_id
      if geonameId != -1:
        lat = ""
        lng = ""
        if "lat" not in row and "lng" not in row:
          lat = float(json.loads(row["geoname_json"])["lat"])
          lng = float(json.loads(row["geoname_json"])["lng"])
        else:
          lat = float(row["lat"])
          lng = float(row["lng"])
        spatial_entity_list.append({"geonameId": geonameId, "lat": lat, "lng": lng})

    neighbors_dict = {}
    for z1 in spatial_entity_list:
      z1_geonameId = z1["geonameId"]
      for z2 in spatial_entity_list:
        z2_geonameId = z2["geonameId"]
        dist = haversine(z1["lng"], z1["lat"], z2["lng"], z2["lat"])
        if z1 != z2 and dist < tresh_distance_in_km:
          if z1_geonameId not in neighbors_dict:
            neighbors_dict[z1_geonameId] = []
          neighbors_dict[z1_geonameId].append(z2_geonameId)
          
    return neighbors_dict
  
  
# spatial scale: "country", "region"
# temporal scale: "week_no", "month_no" 
def preprocessing_for_st_patterns(events, spatial_scale, temporal_scale, TDB_filepath, neighborhood_filepath, tresh_distance_in_km, out_preprocessing_folder):
  SEP = "\t"
  
  # STEP 1: crating neighborhood file for the STEclat algo
  
  geonames_info_filepath = os.path.join(out_preprocessing_folder, spatial_scale+"_geonames_info.csv")
  df_spatial_entity_info = pd.read_csv(geonames_info_filepath, sep=";", keep_default_na=False)
  #print(df_spatial_entity_info.columns)
  geonameId_list = df_spatial_entity_info["geonameId"].to_list() # geonames_id
  geonameId_list = [gId for gId in geonameId_list if gId != -1]
  
  neighbors_dict = get_zone_neighbors(df_spatial_entity_info, tresh_distance_in_km)
  
  if spatial_scale == "country":
    # if it is at country scale, distance based neighborhood is not very accurate.
    # Therefore, we want to improve it with direct neighbors (border sharing)
    country_neighbors_filepath = os.path.join(out_preprocessing_folder, "country_neighbors_info.csv")
    df_country_neighbors = pd.read_csv(country_neighbors_filepath, sep=";", keep_default_na=False)
    
    geonameId_to_neighbors = dict(zip(df_country_neighbors["geonames_id"], df_country_neighbors["neighbors_id"]))
    for geonameId, distanceNeighbors in copy.deepcopy(neighbors_dict).items():
      directNeighbors = geonameId_to_neighbors[geonameId].split(" ")
      directNeighbors = [int(neigh) for neigh in directNeighbors]
      neighbors_dict[geonameId] = list(set(distanceNeighbors + directNeighbors))

  
  file_lines = []
  for key, neighbors in neighbors_dict.items():
    if len(neighbors)>0:
      line_content = str(key) + SEP + SEP.join([str(nid) for nid in neighbors if nid is not None])
      file_lines.append(line_content)
  file_content = "\n".join(file_lines)
  with open(neighborhood_filepath, 'w') as f:
    f.write(file_content)
    
  
  #STEP 2: create temporal database
  year_values = sorted(np.unique([int(e.date.year) for e in events]))
  
  offset = None
  if temporal_scale == "week_no":
    last_week_no_list_by_year = []
    for year in year_values:
      last_week_no = datetime.datetime(year, 12, 28).isocalendar()[1]
      last_week_no_list_by_year.append(last_week_no)
    offset = np.cumsum([0] + last_week_no_list_by_year)
  elif temporal_scale == "month_no":
    offset = np.cumsum([0] + [12]*len(year_values))
  elif temporal_scale == "season_no":
    offset = np.cumsum([0] + [4]*len(year_values))
    
  offset_by_year = dict(zip(year_values, offset[0:len(year_values)]))
  #print(offset_by_year)
  
  country_info_for_interval_events = {}
  for e in events:
    process = True
    if spatial_scale == "region" and e.loc.is_country():
      process = False
    if process: # we skip the events which are not at the right spatial scale
      geonameId = e.loc.hierarchy_data[0] # default: country level
      if spatial_scale == "region":
        geonameId = e.loc.hierarchy_data[1]
      interval_no = e.date.all_interval_info[temporal_scale]
      interval_no = int(interval_no.split("_")[0]) # we remove the year value from the string
      year = e.date.year
      offset = offset_by_year[year]
      period = offset + interval_no
      #print(interval_no, year, offset, period)
      if period not in country_info_for_interval_events:
        country_info_for_interval_events[period] = []
      country_info_for_interval_events[period].append(geonameId)
    
  spatial_entity_info_for_interval_events = dict(sorted(country_info_for_interval_events.items()))
  file_lines = []
  for key, geonameId_list in spatial_entity_info_for_interval_events.items():
    unique_geonameIds = np.unique(geonameId_list)
    unique_geonameIds = [str(c) for c in unique_geonameIds]
    line_content = str(key) + SEP + SEP.join(unique_geonameIds)
    file_lines.append(line_content)
  file_content = "\n".join(file_lines)
  with open(TDB_filepath, 'w') as f:
    f.write(file_content)
  
    
    
    
def extract_st_patterns(TDB_filepath, neighborhood_filepath, minPS, maxIAT, output_filepath):
  ## source: https://github.com/udayRage/PAMI/blob/main/docs/partialPeriodicSpatialPatternMining.md
  ## source: https://github.com/udayRage/PAMI/blob/main/PAMI/partialPeriodicSpatialPattern/basic/STEclat.py
  minPS = minPS
  maxIAT = maxIAT # we can also assign a value by reading the last timestamp from TDB_filepath
  # # -----------------------------
  # # WORKAROUND: STEclat does not return any result when minPS=1.0, because nb total lines is not the same as the nb periodic lines
  # #  So, whenever, a float number is provided, convert it into an integer frequency value
  # if isinstance(minPS, float):
  #   with open(TDB_filepath, 'r') as fp:
  #     nb_total_lines = len(fp.readlines())
  #     print("nb_total_lines:", nb_total_lines)
  #     nb_total_periodic_lines = nb_total_lines-1
  #     minPS = math.floor(minPS * nb_total_periodic_lines)
  # # -----------------------------
  obj = STEclat.STEclat(TDB_filepath, neighborhood_filepath, minPS, maxIAT) # separator is '\t' by default
  obj.startMine() # this outputs: "Spatial Periodic Frequent patterns were generated successfully using SpatialEclat algorithm"
  partialPeriodicSpatialPatterns = obj.getPatterns()
  print("Total number of Periodic Spatial Frequent Patterns:", len(partialPeriodicSpatialPatterns))
  obj.save(output_filepath)
  df = obj.getPatternsAsDataFrame()     #Get the patterns discovered into a dataframe 
  return(df)



def postprocessing_st_pattern_results(df_patterns, df_geonames_info):
  # df_patterns has 2 columns: "Patterns", "periodicSupport"
  
  # location
  geonameId_to_name = dict(zip(df_geonames_info["geonames_id"], df_geonames_info["name"]))
  geonameId_to_country_id = dict(zip(df_geonames_info["geonames_id"], df_geonames_info["country_id"]))
  geonameId_to_country_code = dict(zip(df_geonames_info["geonames_id"], df_geonames_info["country_code"]))
  
  df_patterns["freq"] = df_patterns["periodicSupport"]
  df_patterns["patternsDesc"] = df_patterns["Patterns"].apply(
                lambda x: " ".join([geonameId_to_name[int(a)]+" ("+geonameId_to_country_code[int(a)]+")" 
                       for a in x.strip().split(" ")])
                       )
  
  #df_patterns.sort_values(['country_freq', 'loc_hier_level', 'geonames_id', 'disease_hier_level', 'host_hier_level'], ascending=[False, True, True, True, True], inplace=True)
  df_patterns.sort_values(['freq'], ascending=[False], inplace=True)

  #df_patterns.pop("Patterns")
  df_patterns.pop("periodicSupport")
  return(df_patterns)

    

  