'''
Created on Nov 29, 2022

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



def retrieve_spatial_children_info_by_geonames_id(geonames_id):
  
  print("geonames_id: ", geonames_id)
  # in some way, we could use this one, as well
  # g = geocoder.geonames(main.geonames_id, method='details', key='arinik9', language='en')
  res_dict = {}
  
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
    g = geocoder.geonames(geonames_id, method='children', key=geonames_api_username)
    if g.status == "OK":
      print("status: ", g.status)
      for c in g:
        res_dict[c.geonames_id] = {"geonameId": c.geonames_id, "name": c.address, "latlng": c.latlng, "parentId": geonames_id, "countryId": c.raw["countryId"], "countryCode": c.country_code}
  except:
    print("error in retrieve_spatial_entity_info_info_by_geonames_id() with geonames_id=", geonames_id)
    pass
  print(res_dict)
  return res_dict




def build_spatial_entity_dict(geonames_id_list):
  new_geonames_id_list = []
  spatial_name_list = []
  lat_list = []
  lng_list = []
  country_id_list = []
  country_code_list = []
  parent_id_list = []
  for geonames_id in geonames_id_list:
    children_dict = retrieve_spatial_children_info_by_geonames_id(geonames_id)
    print(geonames_id, len(children_dict))
    if len(children_dict)>0:
      for children_geonames_id, spatial_entity_info in children_dict.items():
        if spatial_entity_info["name"] != "" and len(spatial_entity_info["latlng"])>0:
          spatial_name_list.append(spatial_entity_info["name"])
          lat_list.append(spatial_entity_info["latlng"][0])
          lng_list.append(spatial_entity_info["latlng"][1])
          country_id_list.append(spatial_entity_info["countryId"])
          country_code_list.append(spatial_entity_info["countryCode"])
          parent_id_list.append(spatial_entity_info["parentId"])
          new_geonames_id_list.append(children_geonames_id)
        else:
          print("missing data with geonames_id="+str(geonames_id)+" ....")
      
  df = pd.DataFrame({"geonames_id": new_geonames_id_list, "name": spatial_name_list,\
                      "country_id": country_id_list, "country_code": country_code_list, "lat": lat_list, "lng": lng_list, \
                      "parent_id": parent_id_list})
  return(df)





# if __name__ == '__main__':
#   pass
#
#   input_shapefile_folder = consts.MAP_SHAPEFILE_FOLDER
#   country_geonames_info_filepath = os.path.join(input_shapefile_folder, "world", "country_geonames_info.csv")
#   df_country_geonames_info = pd.read_csv(country_geonames_info_filepath, sep=";", keep_default_na=False)
#   country_geonameId_list = df_country_geonames_info["geonameId"].to_list()
#   country_geonameId_list = [country_id for country_id in country_geonameId_list if country_id != -1]
#
#   df = build_spatial_entity_dict(country_geonameId_list)
#
#   out_folder = consts.OUT_PREPROCESSING_FOLDER
#   result_filepath = os.path.join(out_folder, "ADM1_geonames_info.csv")
#   df.to_csv(result_filepath, sep=";", quoting=csv.QUOTE_NONNUMERIC)

    