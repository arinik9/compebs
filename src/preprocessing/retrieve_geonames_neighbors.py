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

import requests
import json


def retrieve_neighbors_info_by_geonames_id(geonames_id):
  # inspired from: https://atcoordinates.info/2020/10/23/creating-lists-of-country-admin-divisions-with-geonames-and-python/
  
  print("geonames_id: ", geonames_id)
  # in some way, we could use this one, as well
  # g = geocoder.geonames(main.geonames_id, method='details', key='arinik9', language='en')
  res_dict = {"neighbors_id": [], "neighbors_name": []}
  
  
  base_url='http://api.geonames.org/neighboursJSON'
  
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
    
    data_url = f'{base_url}?geonameId={geonames_id}&username={geonames_api_username}'
    print(data_url)
    response=requests.get(data_url)
    if response.ok:
      g = response.json()["geonames"]
      for c in g:
        res_dict["neighbors_id"].append(str(c["geonameId"]))
        res_dict["neighbors_name"].append(c["name"])
  except:
    print("error in retrieve_spatial_entity_info_info_by_geonames_id() with geonames_id=", geonames_id)
    pass
  #print(res_dict)
  return res_dict




def build_spatial_entity_dict(geonames_id_list):
  new_geonames_id_list = []
  neighbors_id_list = []
  neighbors_name_list = []
  for geonames_id in geonames_id_list:
    neighbors_dict = retrieve_neighbors_info_by_geonames_id(geonames_id)
    print(geonames_id, len(neighbors_dict))
    new_geonames_id_list.append(geonames_id)
    if len(neighbors_dict["neighbors_id"])>0 and len(neighbors_dict["neighbors_name"])>0:
      neighbors_id_list.append(" ".join(neighbors_dict["neighbors_id"]))
      neighbors_name_list.append(" ".join(neighbors_dict["neighbors_name"]))
    else:
      neighbors_id_list.append("-1")
      neighbors_name_list.append("-1")
      
  df = pd.DataFrame({"geonames_id": new_geonames_id_list, "neighbors_id": neighbors_id_list,\
                      "neighbors_name": neighbors_name_list})
  return(df)



def create_country_neighbors_info_file(out_preprocessing_folder, force):
  result_filepath = os.path.join(out_preprocessing_folder, "country_neighbors_info.csv")
  if not os.path.exists(result_filepath) or force:

    country_geonames_info_filepath = os.path.join(out_preprocessing_folder, "country_geonames_info.csv")
    df_country_geonames_info = pd.read_csv(country_geonames_info_filepath, sep=";", keep_default_na=False)
    country_geonameId_list = df_country_geonames_info["geonameId"].to_list()
    country_geonameId_list = [country_id for country_id in country_geonameId_list if country_id != -1]
    
    df = build_spatial_entity_dict(country_geonameId_list)
    
    df.to_csv(result_filepath, sep=";", quoting=csv.QUOTE_NONNUMERIC)

    