'''
Created on Nov 30, 2022

@author: nejat
'''



import os
import numpy as np
import pandas as pd
import geopandas as gpd
import csv

import consts

from util import get_total_week_number_of_year

from path import get_spatiotemporal_custom_folder_path

from util_event import read_df_events, read_events_from_df

from plot.plot_event_distribution import plot_event_distribution_generic, comparison_plot_map

from itertools import combinations 

def process_temporal_geo_coverage(out_geoprocessing_folder, events, spatial_scale, temporal_scale, include_prev_and_next_periods=False):
  
  geonames_info_filepath = os.path.join(out_geoprocessing_folder, spatial_scale+"_geonames_info.csv")
  df_spatial_entity_info = pd.read_csv(geonames_info_filepath, sep=";", keep_default_na=False)
  spatial_entity_id_list = list(np.unique(df_spatial_entity_info["geonameId"].to_list()))
  #spatial_entity_id_list = [gId for gId in spatial_entity_id_list if gId != -1]
  
  year_values = sorted(np.unique([int(e.date.year) for e in events]))
  
  periods = []
  for year in year_values:
    TIME_INTERVALS = list(range(1,13))
    if temporal_scale == "week_no":
      nb_weeks = get_total_week_number_of_year(year)
      TIME_INTERVALS = list(range(1,nb_weeks+1))
    for time_interval_no in TIME_INTERVALS:
      period = str(time_interval_no)+"_"+str(year)
      if temporal_scale == "week_no":
        period = str(time_interval_no)+"_"+str(year)
      periods.append(period)
  
  M = np.zeros([len(spatial_entity_id_list), len(periods)], dtype = int)
  df_temporal_geo_coverage = pd.DataFrame(data = M, index = spatial_entity_id_list, columns = periods)
  
  for e in events:
    process = True
    if spatial_scale == "region" and e.loc.is_country():
      process = False
    if process: # we skip the events which are not at the right spatial scale
      geonameId = e.loc.hierarchy_data[0] # default: country level
      if spatial_scale == "region":
        geonameId = e.loc.hierarchy_data[1]
      curr_period = e.date.all_interval_info[temporal_scale]
      indx = periods.index(curr_period)
      prev_period = None
      next_period = None
      if include_prev_and_next_periods and (indx-1) > 0:
        prev_period = periods[indx-1]
      if include_prev_and_next_periods and (indx+1) <= (len(periods)-1):
        next_period = periods[indx+1]

      if geonameId in spatial_entity_id_list:
        if df_temporal_geo_coverage.loc[geonameId, curr_period] == 0:
          df_temporal_geo_coverage.loc[geonameId, curr_period] = 1
        if include_prev_and_next_periods and prev_period is not None and df_temporal_geo_coverage.loc[geonameId, prev_period] == 0:
          df_temporal_geo_coverage.loc[geonameId, prev_period] = 1
        if include_prev_and_next_periods and next_period is not None and df_temporal_geo_coverage.loc[geonameId, next_period] == 0:
          df_temporal_geo_coverage.loc[geonameId, next_period] = 1
        
  return(df_temporal_geo_coverage)      

    
  
def process_similarity_for_temporal_geo_coverage(df_temporal_geo_coverage_ref, df_temporal_geo_coverage_cand):
  # element-wise multiplication
  df_res = df_temporal_geo_coverage_ref.mul(df_temporal_geo_coverage_cand);
  df = df_res.sum(axis=1)/df_temporal_geo_coverage_ref.sum(axis=1)
  df2 = df.fillna(np.nan)
  df3 = df2.to_frame()
  df3.columns = ["temporal_geo_coverage"]
  df3.index.name = "geonameId"
  return df3



def plot_temporal_geo_coverage_in_map_at_region_level(temporal_geo_coverage_result_filepath, region_shapefilepath, out_final_shapefilepath,\
                                            out_map_figure_filepath):

  df_temporal_geo_coverage = pd.read_csv(temporal_geo_coverage_result_filepath, sep=";", keep_default_na=False)
  # df_temporal_geo_coverage["regionMapId"] = df_temporal_geo_coverage["geonameId"].apply(lambda x: geonameId_to_region_map_id[x] if x in geonameId_to_region_map_id else -1)
  #print("what we miss: ", df_temporal_geo_coverage[(df_temporal_geo_coverage["regionMapId"]==-1)&(df_temporal_geo_coverage["temporal_geo_coverage"].notnull())].shape[0], "items")
  #print("what we miss: ", df_temporal_geo_coverage[(df_temporal_geo_coverage["regionMapId"]==-1)&(df_temporal_geo_coverage["temporal_geo_coverage"].notnull())]["geonameId"].to_list())
  geonameId_to_result = dict(zip(df_temporal_geo_coverage["geonameId"], df_temporal_geo_coverage["temporal_geo_coverage"]))

  imd_region = gpd.read_file(region_shapefilepath, encoding = "utf-8")
  imd_region = imd_region.to_crs(4326)
  #imd_region = imd_region.rename(index=str, columns={"diss_me":"ID"})
  imd_region = imd_region.rename(index=str, columns={"gn_id":"ID"})
  #imd_region = imd_region.rename(index=str, columns={"asap0_id":"country_id"})
  column_name = "T_GEO_COV"
  imd_region = imd_region.astype({"ID":'int'})
  imd_region[column_name] = imd_region["ID"].apply(lambda x: geonameId_to_result[x] if x in geonameId_to_result else np.nan)
  imd_region.to_file(driver = 'ESRI Shapefile', filename = out_final_shapefilepath, encoding = "utf-8")

  print(out_final_shapefilepath)
  
  vals = imd_region[column_name].to_numpy()
  float_vals = [float(v) if v != '' else np.nan for v in vals]
  #print(float_vals)
  print(np.nanmean(float_vals))
  
  limits = [0,1]
  continent_name = "world" # to adjust figure size
  display_country_code = True
  display_out_limit_zones = True
  plot_event_distribution_generic(out_final_shapefilepath, out_map_figure_filepath, limits, \
                                       continent_name, column_name, display_country_code, display_out_limit_zones)
  
  
  

def plot_temporal_geo_coverage_in_map_at_country_level(temporal_geo_coverage_result_filepath, country_shapefilepath, out_final_shapefilepath,\
                                            out_map_figure_filepath):
  
  # out_preprocessing_folder = consts.IN_GEONAMES_INFO_FOLDER
  # geonames_info_filepath = os.path.join(out_preprocessing_folder, "country_geonames_info.csv")
  # df_geonames_info = pd.read_csv(geonames_info_filepath, sep=";", keep_default_na=False)
  # geonameId_to_country_map_id = dict(zip(df_geonames_info["geonames_id"], df_geonames_info["country_id"]))
  
  df_temporal_geo_coverage = pd.read_csv(temporal_geo_coverage_result_filepath, sep=";", keep_default_na=False)
  # df_temporal_geo_coverage["countryMapId"] = df_temporal_geo_coverage["geonameId"].apply(lambda x: geonameId_to_country_map_id[x])
  # countryMapId_to_result = dict(zip(df_temporal_geo_coverage["countryMapId"], df_temporal_geo_coverage["temporal_geo_coverage"]))
  geonameId_to_result = dict(zip(df_temporal_geo_coverage["geonameId"], df_temporal_geo_coverage["temporal_geo_coverage"]))


  imd_country = gpd.read_file(country_shapefilepath, encoding = "utf-8")
  imd_country = imd_country.to_crs(4326)
  #imd_country = imd_country.rename(index=str, columns={"asap0_id":"ID"})
  imd_country = imd_country.rename(index=str, columns={"gn_id":"ID"})
  imd_country = imd_country.astype({"ID":'int'})
  imd_country = imd_country.rename(index=str, columns={"isocode":"CNTR_CODE"})
  column_name = "T_GEO_COV"
  imd_country[column_name] = imd_country["ID"].apply(lambda x: geonameId_to_result[x] if x in geonameId_to_result else np.nan)
  imd_country.to_file(driver = 'ESRI Shapefile', filename = out_final_shapefilepath, encoding = "utf-8")
  
  print(out_final_shapefilepath)
  
  vals = imd_country[column_name].to_numpy()
  float_vals = [float(v) if v != '' else np.nan for v in vals]
  #print(float_vals)
  print(np.nanmean(float_vals))
  
  limits = [0,1]
  continent_name = "world" # to adjust figure size
  display_country_code = True
  display_nan_values = True
  plot_event_distribution_generic(out_final_shapefilepath, out_map_figure_filepath, limits, \
                                       continent_name, column_name, display_country_code, display_nan_values)



def plot_temporal_geo_coverage_in_comparison_map_at_country_level(result1_filepath, result2_filepath, \
                                      country_shapefilepath, out_map_figure_filepath):
  limits = [-1,1]
  continent_name = "world" # to adjust figure size
  display_country_code = True
  display_nan_values = True
  column_name = "T_GEO_COV"
  comparison_plot_map(result1_filepath, result2_filepath, out_map_figure_filepath, limits, \
                      continent_name, column_name, display_country_code, display_nan_values)


def plot_temporal_geo_coverage_in_comparison_map_at_region_level(result1_filepath, result2_filepath, \
                                      region_shapefilepath, out_map_figure_filepath):
  limits = [-1,1]
  continent_name = "world" # to adjust figure size
  display_country_code = True
  display_nan_values = True
  column_name = "T_GEO_COV"
  comparison_plot_map(result1_filepath, result2_filepath, out_map_figure_filepath, limits, \
                      continent_name, column_name, display_country_code, display_nan_values)

  
  
def process_temporal_geo_coverage_for_all_platforms(in_events_folder, in_taxonomy_folder, out_folder, out_geoprocessing_folder, platforms, spatial_scales, temporal_scales):
  output_generic_folder = os.path.join(out_folder, "<PLATFORM>")
  # we multiply delay time with 24 because, the delay is expressed in hours for practical reasons in STEclat algo
  for platform in platforms:
    for spatial_scale in spatial_scales:
      for temporal_scale in temporal_scales:
        output_result_folder = get_spatiotemporal_custom_folder_path(output_generic_folder, platform, \
                                                       spatial_scale=spatial_scale, temporal_scale=temporal_scale)
  
        result_filename_suffix = "platform="+platform+"_"+spatial_scale+"_"+temporal_scale
  
        try:
          if not os.path.exists(output_result_folder):
            os.makedirs(output_result_folder)
        except OSError as err:
          print(err)
  
        input_event_folder = os.path.join(in_events_folder, platform)

        events_filepath = os.path.join(input_event_folder, "events.csv")
        df_events = read_df_events(events_filepath)
        events = read_events_from_df(df_events, in_taxonomy_folder)
  
        include_prev_and_next_periods = True
        if platform == consts.NEWS_DB_EMPRESS_I:
          include_prev_and_next_periods = False
        df_temporal_geo_coverage = process_temporal_geo_coverage(out_geoprocessing_folder, events, spatial_scale, temporal_scale, include_prev_and_next_periods)
  
        final_result_filename = "temporal_geo_event_presence_" + result_filename_suffix + ".csv"
        out_temporal_geo_coverage_filepath = os.path.join(output_result_folder, final_result_filename)
        df_temporal_geo_coverage.to_csv(out_temporal_geo_coverage_filepath, sep=";", quoting=csv.QUOTE_NONNUMERIC)



def plot_temporal_geo_coverage_results_for_all_platforms(in_folder, out_folder, input_shapefile_folder, ref_platform, platforms, spatial_scales, temporal_scales):
  input_generic_folder = os.path.join(in_folder, "<PLATFORM>")
  output_generic_folder = os.path.join(out_folder, "<PLATFORM>")
  
  for platform in platforms:
    for spatial_scale in spatial_scales:
      for temporal_scale in temporal_scales:
        input_folder = get_spatiotemporal_custom_folder_path(input_generic_folder, platform, \
                                                       spatial_scale=spatial_scale, temporal_scale=temporal_scale)
        result_filename_suffix = "platform="+platform+"_"+spatial_scale+"_"+temporal_scale
        result_filename = "temporal_geo_event_presence_" + result_filename_suffix + ".csv"
        result_filepath = os.path.join(input_folder, result_filename)
        df_temporal_geo_coverage = pd.read_csv(result_filepath, sep=";", keep_default_na=False, index_col=0)
        print(result_filepath)
        
        input_folder = get_spatiotemporal_custom_folder_path(input_generic_folder, ref_platform, \
                                                       spatial_scale=spatial_scale, temporal_scale=temporal_scale)
        result_filename_suffix = "platform="+ref_platform+"_"+spatial_scale+"_"+temporal_scale
        result_filename = "temporal_geo_event_presence_" + result_filename_suffix + ".csv"
        result_filepath = os.path.join(input_folder, result_filename)
        df_temporal_geo_coverage_ref = pd.read_csv(result_filepath, sep=";", keep_default_na=False, index_col=0)
        print(result_filepath)
  
        # ------------------------
  
        df_result = process_similarity_for_temporal_geo_coverage(df_temporal_geo_coverage_ref, df_temporal_geo_coverage)
  
        platform_pair = platform+"_vs_"+ref_platform
        result_filename_suffix = "platform="+platform_pair+"_"+spatial_scale+"_"+temporal_scale
        output_folder = get_spatiotemporal_custom_folder_path(output_generic_folder, platform_pair, \
                                                       spatial_scale=spatial_scale, temporal_scale=temporal_scale)
        try:
          if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        except OSError as err:
          print(err)
  
        final_result_filename = "final_temporal_geo_coverage_" + result_filename_suffix + ".csv"
        out_temporal_geo_coverage_results_filepath = os.path.join(output_folder, final_result_filename)
        df_result.to_csv(out_temporal_geo_coverage_results_filepath, sep=";", quoting=csv.QUOTE_NONNUMERIC)        
  
        if spatial_scale == "country":
          # REMARK: only at country level, beacause we need to associate map regions ids with
          #   geoname ids >> can be difficult for regions, since we need to geocode region names, not so easy
          country_shapefilepath = os.path.join(input_shapefile_folder, "world", "gaul0_asap", "gaul0_asap.shp")
          final_result_filename = "final_temporal_geo_coverage_" + result_filename_suffix + ".shp"
          out_final_shapefilepath = os.path.join(output_folder, final_result_filename)
          final_result_filename = "final_temporal_geo_coverage_" + result_filename_suffix + ".png"
          out_map_figure_filepath = os.path.join(output_folder, final_result_filename)
          plot_temporal_geo_coverage_in_map_at_country_level(out_temporal_geo_coverage_results_filepath, country_shapefilepath, out_final_shapefilepath,\
                                              out_map_figure_filepath)
  
        elif spatial_scale == "region":
          region_shapefilepath = os.path.join(input_shapefile_folder, "world", "ne_10m_admin_1_states_provinces", "naturalearth_adm1.shp")
          #region_shapefilepath = os.path.join(input_shapefile_folder, "world", "gadm", "gadm36_1.shp")
          final_result_filename = "final_temporal_geo_coverage_" + result_filename_suffix + ".shp"
          out_final_shapefilepath = os.path.join(output_folder, final_result_filename)
          final_result_filename = "final_temporal_geo_coverage_" + result_filename_suffix + ".png"
          out_map_figure_filepath = os.path.join(output_folder, final_result_filename)
          plot_temporal_geo_coverage_in_map_at_region_level(out_temporal_geo_coverage_results_filepath, region_shapefilepath, out_final_shapefilepath,\
                                              out_map_figure_filepath)
          
          

def plot_temporal_geo_coverage_result_comparison_for_all_platforms(in_folder, out_folder, input_shapefile_folder, platforms, ref_platform, spatial_scales, temporal_scales):
  input_generic_folder = os.path.join(in_folder, "<PLATFORM>")
  output_generic_folder = os.path.join(out_folder, "<PLATFORM>")
  
  for platform_pair in list(combinations(platforms, 2)):
    for spatial_scale in spatial_scales:
      for temporal_scale in temporal_scales:
        platform_pair_desc = platform_pair[0]+"_vs_"+ref_platform
        result_filename_suffix = "platform="+platform_pair_desc+"_"+spatial_scale+"_"+temporal_scale
        input_folder = get_spatiotemporal_custom_folder_path(input_generic_folder, platform_pair_desc, \
                                                       spatial_scale=spatial_scale, temporal_scale=temporal_scale)
        final_result_filename = "final_temporal_geo_coverage_" + result_filename_suffix + ".shp"
        padiweb_temporal_geo_coverage_results_filepath = os.path.join(input_folder, final_result_filename)
        print(padiweb_temporal_geo_coverage_results_filepath)
        
        platform_pair_desc = platform_pair[1]+"_vs_"+ref_platform
        result_filename_suffix = "platform="+platform_pair_desc+"_"+spatial_scale+"_"+temporal_scale
        input_folder = get_spatiotemporal_custom_folder_path(input_generic_folder, platform_pair_desc, \
                                                       spatial_scale=spatial_scale, temporal_scale=temporal_scale)
        final_result_filename = "final_temporal_geo_coverage_" + result_filename_suffix + ".shp"
        promed_temporal_geo_coverage_results_filepath = os.path.join(input_folder, final_result_filename)
        print(promed_temporal_geo_coverage_results_filepath)
        
        out_platform_pair_desc = platform_pair[0]+"_vs_"+platform_pair[1]
        output_folder = get_spatiotemporal_custom_folder_path(output_generic_folder, out_platform_pair_desc, \
                                                       spatial_scale=spatial_scale, temporal_scale=temporal_scale)
        
        try:
          if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        except OSError as err:
          print(err)
        
        if spatial_scale == "country":
          # REMARK: only at country level, beacause we need to associate map regions ids with
          #   geoname ids >> can be difficult for regions, since we need to geocode region names, not so easy
          result_filename_suffix = "platform="+out_platform_pair_desc+"_on="+ref_platform+"_"+spatial_scale+"_"+temporal_scale
          country_shapefilepath = os.path.join(input_shapefile_folder, "world", "gaul0_asap", "gaul0_asap.shp")
          final_result_filename = "final_temporal_geo_coverage_" + result_filename_suffix + ".png"
          out_map_figure_filepath = os.path.join(output_folder, final_result_filename)
          plot_temporal_geo_coverage_in_comparison_map_at_country_level(\
                   padiweb_temporal_geo_coverage_results_filepath, promed_temporal_geo_coverage_results_filepath,\
                   country_shapefilepath, out_map_figure_filepath)
    
        elif spatial_scale == "region":
          # REMARK: only at country level, beacause we need to associate map regions ids with
          #   geoname ids >> can be difficult for regions, since we need to geocode region names, not so easy
          result_filename_suffix = "platform="+out_platform_pair_desc+"_on="+ref_platform+"_"+spatial_scale+"_"+temporal_scale
          region_shapefilepath = os.path.join(input_shapefile_folder, "world", "ne_10m_admin_1_states_provinces", "naturalearth_adm1.shp")
          final_result_filename = "final_temporal_geo_coverage_" + result_filename_suffix + ".png"
          out_map_figure_filepath = os.path.join(output_folder, final_result_filename)
          plot_temporal_geo_coverage_in_comparison_map_at_region_level(\
                   padiweb_temporal_geo_coverage_results_filepath, promed_temporal_geo_coverage_results_filepath,\
                   region_shapefilepath, out_map_figure_filepath)
      


def compute_final_temporal_geo_coverage_result_comparison_for_all_platforms(in_folder, out_folder, platforms, ref_platform, spatial_scales, temporal_scales):
  input_generic_folder = os.path.join(in_folder, "<PLATFORM>")
  output_generic_folder = os.path.join(out_folder, "<PLATFORM>")
  
  for platform_name in platforms:
    res_dict = {}

    for spatial_scale in spatial_scales:
      for temporal_scale in temporal_scales:
        platform_pair_desc = platform_name+"_vs_"+ref_platform
        result_filename_suffix = "platform="+platform_pair_desc+"_"+spatial_scale+"_"+temporal_scale
        input_folder = get_spatiotemporal_custom_folder_path(input_generic_folder, platform_pair_desc, \
                                                       spatial_scale=spatial_scale, temporal_scale=temporal_scale)
        final_result_filename = "final_temporal_geo_coverage_" + result_filename_suffix + ".csv"
        platform_temporal_geo_coverage_results_filepath = os.path.join(input_folder, final_result_filename)
        print(platform_temporal_geo_coverage_results_filepath)
        df_result = pd.read_csv(platform_temporal_geo_coverage_results_filepath, sep=";", keep_default_na=False)
        geo_coverage_results = df_result["temporal_geo_coverage"].to_numpy()
        geo_coverage_results = geo_coverage_results[geo_coverage_results != ''].astype(float)
        res_dict[platform_temporal_geo_coverage_results_filepath] = np.mean(geo_coverage_results)
        
    output_folder = get_spatiotemporal_custom_folder_path(output_generic_folder, platform_name)
    df_all = pd.DataFrame.from_dict(res_dict, orient='index', columns=["temporal_geocoverage"])
    res_eval_filename = "all_temporal_geo_coverage_results_platform="+platform_name+".csv"
    res_eval_filepath = os.path.join(output_folder, res_eval_filename)
    df_all.to_csv(res_eval_filepath, sep=";", quoting=csv.QUOTE_NONNUMERIC)      



