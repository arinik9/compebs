'''
Created on Oct 5, 2022

@author: nejat
'''

import geopandas as gpd
import os
import consts
import json
import pandas as pd
import csv
from iso3166 import countries
from geopy.geocoders import GeoNames



# the variable 'country_bias_list' contains country alpha2 codes
def geocode_batch_with_geonames(spatial_entity_list, country_bias_list):

  result_list = []
  for i in range(len(spatial_entity_list)):
    res = {"geonameId": "-1", "name": "-1", "country_code": "-1", "raw_data": "-1"}
    try:
      name = spatial_entity_list[i]
      country_bias = country_bias_list[i]
      if country_bias == "-1":
        country_bias=None
      #else:
      #  country_bias = countries.get(country_bias).alpha2
      print(i, name, country_bias)
      
      client_geonames = GeoNames(username=consts.GEONAMES_API_USERNAME)
      geonames_locations = client_geonames.geocode(name, exactly_one=False)
      if geonames_locations is None:
        geonames_locations = []
      best_loc = None
      processed = False
      for loc in geonames_locations:
        if loc != -1 and "countryCode" in loc and loc["countryCode"] in country_bias:
          best_loc = loc
          processed = True
          break
      if not processed and len(geonames_locations)>0:
        best_loc = geonames_locations[0] # by deafult
      
      if best_loc is not None:
        if best_loc.raw["geonameId"] != best_loc.raw["countryId"]: # we do not want to get a country
          print(best_loc.raw)
          best_loc_name = best_loc.raw["toponymName"]
          best_loc_country_code = best_loc.raw["countryCode"]
          print(best_loc_country_code)
          best_loc_country_code = countries.get(best_loc_country_code).alpha3 
          res = {"geonameId": best_loc.raw["geonameId"], "name": best_loc_name, "country_code": best_loc_country_code, "raw_data": best_loc.raw}
    except:
      print("error in geocode_batch_with_geonames() with name=", spatial_entity_list[i])
      pass
    result_list.append(res)
    
  return result_list



def retrieve_geonames_id_for_countries(in_map_shapefile_folder, out_preprocessing_folder, force):
  output_filepath = os.path.join(out_preprocessing_folder, "country_geonames_info.csv")
  if not os.path.exists(output_filepath) or force:
  
    try:
      if not os.path.exists(out_preprocessing_folder):
        os.makedirs(out_preprocessing_folder)
    except OSError as err:
       print(err)
    
    country_map_shapefilepath = os.path.join(in_map_shapefile_folder, "world/gaul0_asap/gaul0_asap.shp")
    world_map_data = gpd.read_file(country_map_shapefilepath, encoding = "utf-8")
    world_map_data = world_map_data.to_crs(4326)
    world_map_data = world_map_data.rename(index=str, columns={"name0":"country"})
    world_map_data = world_map_data.rename(index=str, columns={"asap0_id":"country_id"})
    
    spatial_entity_list = world_map_data["country"].to_list()
    country_bias_list = world_map_data["isocode"].to_list()
    res_list = geocode_batch_with_geonames(spatial_entity_list, country_bias_list)
    geonames_id_list = []
    geonames_raw_data_list = []
    fcode_list = []
    for res in res_list:
      geonames_id_list.append(res["geonameId"])
      geonames_raw_data_list.append(json.dumps(res["raw_data"]))
      fcode = ""
      if "fcode" in res["raw_data"]:
        fcode = res["raw_data"]["fcode"]
      fcode_list.append(fcode)
  
    country_id_list = world_map_data["country_id"].to_list()
    df = pd.DataFrame({"country_id": country_id_list, "country_name":spatial_entity_list, "geonameId": geonames_id_list, \
                       "geoname_json": geonames_raw_data_list, "fcode": fcode_list})
    
    df.to_csv(output_filepath, sep=";", quoting=csv.QUOTE_NONNUMERIC)
  
  