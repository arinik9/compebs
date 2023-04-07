'''
Created on Nov 23, 2022

@author: nejat
'''

import consts
from random import randrange
import os
from util_event import read_df_events, read_events_from_df

import numpy as np
import csv
import geocoder # >>> https://geocoder.readthedocs.io/providers/GeoNames.html

import pandas as pd




def retrieve_spatial_entity_info_info_by_geonames_id(geonames_id):
  # g = geocoder.geonames(main.geonames_id, method='details', key='arinik9', language='en')
  
  print("geonames_id: ", geonames_id)
  # in some way, we could use this one, as well
  # g = geocoder.geonames(main.geonames_id, method='details', key='arinik9', language='en')
  res = {"name": "", "latlng": []}
  
  geonames_api_username_list = [consts.GEONAMES_API_USERNAME, consts.GEONAMES_API_USERNAME2, \
                                consts.GEONAMES_API_USERNAME3, consts.GEONAMES_API_USERNAME4, \
                                consts.GEONAMES_API_USERNAME5, consts.GEONAMES_API_USERNAME6, \
                                consts.GEONAMES_API_USERNAME7]
  try:
    # there are some hourly and daily query limit for geonames servers.
    # as a workaround, we randomly pick one account and send our request. 
    # >> in theory, those accounts will be picked approx. uniformly
    rand_index = randrange(len(geonames_api_username_list))
    geonames_api_username = geonames_api_username_list[rand_index]
    print("---- account ", geonames_api_username)
    g = geocoder.geonames(geonames_id, method='hierarchy', key=geonames_api_username)
    if g.status == "OK":
      print("status: ", g.status)
      hier_level = len(g)-1 # since levels start from 0
      res["hier_level"] = hier_level
      result = g[-1]
      print(result.raw)
      res["name"] = result.address
      res["latlng"] = result.latlng
      res["countryId"] = result.raw["countryId"]
      res["countryCode"] = result.country_code
  except:
    print("error in retrieve_spatial_entity_info_info_by_geonames_id() with geonames_id=", geonames_id)
    pass
  print(res)
  return res




def build_spatial_entity_dict(geonames_id_list):
  new_geonames_id_list = []
  spatial_name_list = []
  lat_list = []
  lng_list = []
  country_id_list = []
  country_code_list = []
  hier_level_list = []
  for geonames_id in geonames_id_list:
    spatial_entity_info = retrieve_spatial_entity_info_info_by_geonames_id(geonames_id)
    if spatial_entity_info["name"] != "" and len(spatial_entity_info["latlng"])>0 and "countryId" in spatial_entity_info:
      spatial_name_list.append(spatial_entity_info["name"])
      lat_list.append(spatial_entity_info["latlng"][0])
      lng_list.append(spatial_entity_info["latlng"][1])
      country_id_list.append(spatial_entity_info["countryId"])
      country_code_list.append(spatial_entity_info["countryCode"])
      hier_level_list.append(spatial_entity_info["hier_level"])
      new_geonames_id_list.append(geonames_id)
    else:
      print("missing data with geonames_id="+str(geonames_id)+" ....")
      
  df = pd.DataFrame({"geonames_id": new_geonames_id_list, "name": spatial_name_list,\
                      "country_id": country_id_list, "country_code": country_code_list, "lat": lat_list, "lng": lng_list, \
                      "hier_level": hier_level_list})
  return(df)




def create_single_geonames_info_file_from_all_events(in_taxonomy_folder, events_filepath_padiweb, events_filepath_promed, events_filepath_empresi, out_folder, force):

  df_events = read_df_events(events_filepath_padiweb)
  padiweb_events = read_events_from_df(df_events, in_taxonomy_folder)
  
  df_events = read_df_events(events_filepath_promed)
  promed_events = read_events_from_df(df_events, in_taxonomy_folder)

  df_events = read_df_events(events_filepath_empresi)
  empresi_events = read_events_from_df(df_events, in_taxonomy_folder)
  
  events = padiweb_events + promed_events + empresi_events
  
  result_filepath = os.path.join(out_folder, "geonames_info.csv")
  
  if not os.path.exists(result_filepath) or force:
  
    try:
      if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    except OSError as err:
      print(err)
    
    geonames_id_list = []
    for e in events:
      geonames_id_list = geonames_id_list + e.loc.hierarchy_data
    unique_geonames_id_list = np.unique(geonames_id_list)
    
    df = build_spatial_entity_dict(unique_geonames_id_list)
    df.to_csv(result_filepath, sep=";", quoting=csv.QUOTE_NONNUMERIC)

  