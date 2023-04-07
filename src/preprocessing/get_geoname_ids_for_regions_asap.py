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
def geocode_batch_with_geonames(spatial_entity_list, country_code_list, feature_code):

  base_url='http://api.geonames.org/searchJSON'
  
  geonames_api_username_list = [consts.GEONAMES_API_USERNAME2, \
                                consts.GEONAMES_API_USERNAME3, consts.GEONAMES_API_USERNAME4, \
                                consts.GEONAMES_API_USERNAME5, consts.GEONAMES_API_USERNAME6, \
                                consts.GEONAMES_API_USERNAME7] # consts.GEONAMES_API_USERNAME, 
  
  result_list = []
  for i in range(len(spatial_entity_list)):
    
    res = {"geonameId": "-1", "name": "-1", "country_code": "-1", "raw_data": "-1"}
    name = spatial_entity_list[i]
    country_code = country_code_list[i]
    if country_code == "-1":
      country_code=None
    print(i, name, country_code)
    
    try:
      # there are some hourly and daily query limit for geonames servers.
      # as a workaround, we randomly pick one account and send our request. 
      # >> in theory, those accounts will be picked approx. uniformly
      rand_index = randrange(len(geonames_api_username_list))
      geonames_api_username = geonames_api_username_list[rand_index]
      print("---- account ", geonames_api_username)
      
      data_url = f'{base_url}?q={name}&country={country_code}&featureCode={feature_code}&username={geonames_api_username}'
      print(data_url)
      response=requests.get(data_url)
      response_json_data = response.json()["geonames"]
      if response.ok and len(response_json_data)>0:
        #for g in response_json_data:
        g = response_json_data[0]
        res = {"geonameId": g["geonameId"], "name": name, "country_code": country_code, "raw_data": g}
        print(res)
    except:
      print("error in retrieve_spatial_entity_info_info_by_geonames_id() with name=", name,"with country=",country_code)
    result_list.append(res)
    
  return result_list




def retrieve_geonames_id_for_regions_from_asap(in_map_shapefile_folder, out_preprocessing_folder, force):
  output_filepath = os.path.join(out_preprocessing_folder, "region_geonames_info.csv")
  if not os.path.exists(output_filepath) or force:

    geonames_info_filepath = os.path.join(out_preprocessing_folder, "country_geonames_info.csv")
    df_geonames_info = pd.read_csv(geonames_info_filepath, sep=";", keep_default_na=False)
    df_geonames_info["country_code"] = df_geonames_info["geoname_json"].apply(lambda x: json.loads(x)['countryCode'] if json.loads(x) != "-1" else "-1")
    id_to_country_code = dict(zip(df_geonames_info["country_id"], df_geonames_info["country_code"]))
    
    region_map_shapefilepath = os.path.join(in_map_shapefile_folder, "world/gaul1_asap/gaul1_asap.shp")
    world_map_data = gpd.read_file(region_map_shapefilepath, encoding = "utf-8")
    world_map_data = world_map_data.to_crs(4326)
    world_map_data = world_map_data.rename(index=str, columns={"asap1_id":"ID"})
    world_map_data = world_map_data.rename(index=str, columns={"name1":"region"})
    world_map_data = world_map_data.rename(index=str, columns={"name0":"country"})
    world_map_data = world_map_data.rename(index=str, columns={"asap0_id":"country_id"})
    world_map_data["desc"] = world_map_data["region"] + ", " + world_map_data["country"]
    world_map_data["country_code"] = world_map_data["country_id"].apply(lambda x: id_to_country_code[x])
    
    spatial_entity_list = world_map_data["region"].to_list()
    country_name_list = world_map_data["country"].to_list()
    country_code_list = world_map_data["country_code"].to_list()
    res_list = geocode_batch_with_geonames(spatial_entity_list, country_code_list, 'ADM1')
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
  
    region_id_list = world_map_data["ID"].to_list()
    df = pd.DataFrame({"region_id": region_id_list, "region_name":spatial_entity_list, "country_code": country_code_list, "country_name": country_name_list, "geonameId": geonames_id_list, \
                       "geoname_json": geonames_raw_data_list, "fcode": fcode_list})
    
    df.to_csv(output_filepath, sep=";", quoting=csv.QUOTE_NONNUMERIC)
  
  
  
  
def retrieve_geonames_id_for_regions_from_gadm(in_map_shapefile_folder, out_preprocessing_folder, force):
  output_filepath = os.path.join(out_preprocessing_folder, "region_geonames_info.csv")

  if not os.path.exists(output_filepath) or force:

    region_map_csv_filepath = os.path.join(in_map_shapefile_folder, "world/gadm/gadm36_1.csv")
    df_map_regions = pd.read_csv(region_map_csv_filepath, sep=";", keep_default_na=False)
    df_map_regions["country_code"] = df_map_regions["GID_0"].apply(lambda x: retrieve_country_alpha2_code_from_alpha3_code(x))
    #df_map_regions = df_map_regions.loc[df_map_regions["country_code"] == "IT",:]
  
    spatial_entity_list = df_map_regions["NAME_1"].to_list()
    spatial_entity_alternative_name_list = df_map_regions["VARNAME_1"].to_list()
    spatial_entity_list_of_list = []
    for i in range(len(spatial_entity_list)):
      item = [spatial_entity_list[i]]
      if len(spatial_entity_alternative_name_list[i])>0:
        item = item + spatial_entity_alternative_name_list[i].split("|")
      spatial_entity_list_of_list.append(item)
    #print(spatial_entity_list_of_list)
  
    country_name_list = df_map_regions["COUNTRY"].to_list()
    country_code_list = df_map_regions["country_code"].to_list()
    lat_list = df_map_regions["lat"].to_list()
    lng_list = df_map_regions["lng"].to_list()
    res_list = geocode_batch_with_geonames(spatial_entity_list_of_list, country_code_list, 'ADM1', lat_list, lng_list)
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
  
    region_id_list = df_map_regions["GID_1"].to_list()
    df = pd.DataFrame({"region_id": region_id_list, "region_name":spatial_entity_list, "country_code": country_code_list, "country_name": country_name_list, "geonameId": geonames_id_list, \
                       "geoname_json": geonames_raw_data_list, "fcode": fcode_list})
    
    df.to_csv(output_filepath, sep=";", quoting=csv.QUOTE_NONNUMERIC)
  
  