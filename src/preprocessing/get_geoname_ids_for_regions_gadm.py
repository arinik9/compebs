'''
Created on Dec 1, 2022

@author: nejat
'''


import geopandas as gpd
import os
import consts
import json
import pandas as pd
import csv

from random import randrange
import requests
from util_gis import haversine, retrieve_country_alpha2_code_from_alpha3_code


# the variable 'country_bias_list' contains country alpha2 codes
def geocode_batch_with_geonames(spatial_entity_list_of_list, country_code_list, feature_code, lat_list, lng_list):

  base_url='http://api.geonames.org/searchJSON'
  
  geonames_api_username_list = [consts.GEONAMES_API_USERNAME, consts.GEONAMES_API_USERNAME2, \
                                consts.GEONAMES_API_USERNAME3, consts.GEONAMES_API_USERNAME4, \
                                consts.GEONAMES_API_USERNAME5, consts.GEONAMES_API_USERNAME6, \
                                consts.GEONAMES_API_USERNAME7]
  
  result_list = []
  for i in range(len(spatial_entity_list_of_list)):
    spatial_entity_name_list = spatial_entity_list_of_list[i]
    res = {"geonameId": "-1", "name": "-1", "country_code": "-1", "raw_data": "-1"}
    country_code = country_code_list[i]
    if country_code == "-1":
      country_code=None
    lat = float(lat_list[i])
    lng = float(lng_list[i])
    
    for spatial_entity_name in spatial_entity_name_list:
      try:
        # there are some hourly and daily query limit for geonames servers.
        # as a workaround, we randomly pick one account and send our request. 
        # >> in theory, those accounts will be picked approx. uniformly
        rand_index = randrange(len(geonames_api_username_list))
        geonames_api_username = geonames_api_username_list[rand_index]
        print("---- account ", geonames_api_username)
        
        data_url = f'{base_url}?q={spatial_entity_name}&country={country_code}&featureCode={feature_code}&username={geonames_api_username}'
        print(data_url)
        response=requests.get(data_url)
        response_json_data = response.json()["geonames"]
        if response.ok and len(response_json_data)>0:
          dist = 1000000 # something very large
          best_loc = None
          for g in response_json_data:
            cat_lat = float(g["lat"])
            cat_lng = float(g["lng"])
            new_dist = haversine(lng, lat, cat_lng, cat_lat)
            if new_dist < dist:
              best_loc = g
          res = {"geonameId": best_loc["geonameId"], "name": spatial_entity_name, "country_code": country_code, "raw_data": best_loc}
          break
      except:
        print("error in retrieve_spatial_entity_info_info_by_geonames_id() with name=", spatial_entity_name,"with country=",country_code)
    result_list.append(res)
    
  return result_list





  