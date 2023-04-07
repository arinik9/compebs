'''
Created on Apr 5, 2023

@author: nejat
'''

import os
import pandas as pd
import csv
import math
import numpy as np


from temporal_analysis.st_motifs.extract_st_motifs import preprocessing_for_st_patterns, extract_st_patterns, postprocessing_st_pattern_results
from path import get_spatiotemporal_custom_folder_path
from util_event import read_df_events, read_events_from_df



def process_continuous_periodic_st_motif_extraction(in_folder, in_taxonomy_folder, out_folder, platform_name, out_preprocessing_folder, spatial_scales, temporal_scales):
  out_folder_platform = os.path.join(out_folder, "<PLATFORM>")
  output_dirpath_platform = out_folder_platform
  
  minPS_values = [0.1] # 0.2, 0.3, 0.4, 0.5
  maxIAT_values = [2] # expressed in the selected temporal scale, e.g. 1 week
  tresh_distance_in_km_values = [1000] # , 1500, 2000
  
  # we multiply delay time with 24 because, the delay is expressed in hours for practical reasons in STEclat algo
  for spatial_scale in spatial_scales:
    for temporal_scale in temporal_scales:
      for tresh_distance_in_km in tresh_distance_in_km_values:
        for minPS in minPS_values:
          for maxIAT in maxIAT_values:
            output_result_folder = get_spatiotemporal_custom_folder_path(output_dirpath_platform, platform_name, \
                                                           spatial_scale=spatial_scale, temporal_scale=temporal_scale)
            
            result_filename_suffix = "minPS="+str(minPS)
            result_filename_suffix += "_maxIAT="+str(maxIAT)
            result_filename_suffix += "_maxDist="+str(tresh_distance_in_km)
            result_filename_suffix += "_platform="+platform_name
            
            print(output_result_folder, result_filename_suffix)
            
            try:
              if not os.path.exists(output_result_folder):
                os.makedirs(output_result_folder)
            except OSError as err:
              print(err)
              
            raw_result_filename = "raw_st_motifs_" + result_filename_suffix + ".txt"
            #if not os.path.exists(raw_result_filename):

            input_folder = os.path.join(in_folder, platform_name)
            events_filepath = os.path.join(input_folder, "events.csv")
            df_events = read_df_events(events_filepath)
            events = read_events_from_df(df_events, in_taxonomy_folder)

            geonames_info_filepath = os.path.join(out_preprocessing_folder, "geonames_info.csv")
            df_geonames_info = pd.read_csv(geonames_info_filepath, sep=";", keep_default_na=False)
            #geonameId_to_name = dict(zip(df_geonames_info["geonames_id"], df_geonames_info["name"]))

            TDB_filepath = os.path.join(output_result_folder, "TDB_"+result_filename_suffix+".txt")
            neighborhood_filepath = os.path.join(output_result_folder, "neighborhood_"+result_filename_suffix+".txt")
            
            preprocessing_for_st_patterns(events, spatial_scale, temporal_scale, TDB_filepath, neighborhood_filepath, tresh_distance_in_km, out_preprocessing_folder)
            
            
            output_filepath = os.path.join(output_result_folder, raw_result_filename)
            df_patterns = extract_st_patterns(TDB_filepath, neighborhood_filepath, minPS, maxIAT, output_filepath)
            print(df_patterns)
            
            
            print("-------------")
            
            if len(df_patterns) == 0 or df_patterns.shape[0] == 0:
              df_patterns = pd.DataFrame() 
            else:
              df_patterns = postprocessing_st_pattern_results(df_patterns, df_geonames_info)
              print(df_patterns)
            
            final_result_filename = "continuous_periodic_st_motifs_" + result_filename_suffix + ".csv"
            out_pattern_results_filepath = os.path.join(output_result_folder, final_result_filename)
            df_patterns.to_csv(out_pattern_results_filepath, sep=";", quoting=csv.QUOTE_NONNUMERIC)



def process_seasonal_periodic_st_motif_extraction(in_folder, in_taxonomy_folder, out_folder, platform_name, out_preprocessing_folder, spatial_scales, temporal_scales):

  geonames_info_filepath = os.path.join(out_preprocessing_folder, "geonames_info.csv")
  df_geonames_info = pd.read_csv(geonames_info_filepath, sep=";", keep_default_na=False)
              
  out_folder_platform = os.path.join(out_folder, "<PLATFORM>")
  output_dirpath_platform = out_folder_platform
  

  minPS_values = [0.5, 1.0] # 0.5: partial periodicity and 1.0: full periodicity
  #maxIAT = 1 # expressed in the selected temporal scale, e.g. 1 week
  tresh_distance_in_km_values = [1000] # , 1500, 2000
  
  # we multiply delay time with 24 because, the delay is expressed in hours for practical reasons in STEclat algo
  for spatial_scale in spatial_scales:
    for temporal_scale in temporal_scales:
      for minPS in minPS_values:
        for tresh_distance_in_km in tresh_distance_in_km_values:
            output_result_folder = get_spatiotemporal_custom_folder_path(output_dirpath_platform, platform_name, \
                                                           spatial_scale=spatial_scale, temporal_scale=temporal_scale)
            result_filename_suffix = "minPS="+str(minPS)+"_maxDist="+str(tresh_distance_in_km)
            result_filename_suffix += "_platform="+platform_name
            print(output_result_folder, result_filename_suffix)
            
            try:
              if not os.path.exists(output_result_folder):
                os.makedirs(output_result_folder)
            except OSError as err:
              print(err)
              
              
            time_interval_no_list = None
            if temporal_scale == "month_no":
              time_interval_no_list = list(range(1,13)) # monthly
            elif temporal_scale == "season_no":
              time_interval_no_list = list(range(1,5)) # monthly
              
              
            df_patterns_list = []
            for time_interval_no in time_interval_no_list:
              print("time_interval_no", time_interval_no)
              input_folder = os.path.join(in_folder, platform_name)
              events_filepath = os.path.join(input_folder, "events.csv")
              df_events = read_df_events(events_filepath)
              
              year_values = sorted(np.unique([int(y) for y in df_events["year"].to_list()]))
              
              # ============================
              # Filter
              df_events = df_events[df_events[temporal_scale+"_simple"] == time_interval_no]
              print("nb:", df_events.shape)
              # ============================
              #print(df_events)
              
              events = read_events_from_df(df_events, in_taxonomy_folder)
              
              temp_raw_result_filename = "temp.txt"
              temp_TDB_filepath = os.path.join(output_result_folder, "temp_TDB.txt")
              temp_neighborhood_filepath = os.path.join(output_result_folder, "temp_neighborhood.txt")
              
              preprocessing_for_st_patterns(events, spatial_scale, temporal_scale, temp_TDB_filepath, temp_neighborhood_filepath, tresh_distance_in_km, out_preprocessing_folder)
              
              output_filepath = os.path.join(output_result_folder, temp_raw_result_filename)
              
              
              print(year_values)
              nb_total_lines = len(year_values)
              nb_total_periodic_lines = nb_total_lines-1
              minPS_freq = math.floor(minPS * nb_total_periodic_lines)
              #minPS = (len(year_values)-1) # -1 because of periodicity (cyclic behavior) >> full periodicity
              #minPS = (len(year_values)-2) # >> partial periodicity
              #minPS = 1
              maxIAT = len(time_interval_no_list) # in terms of 'temporal_scale'
              df_patterns = extract_st_patterns(temp_TDB_filepath, temp_neighborhood_filepath, minPS_freq, maxIAT, output_filepath)
              if len(df_patterns) > 0 and df_patterns.shape[0] > 0:
                df_patterns[temporal_scale] = time_interval_no
                df_patterns_list.append(df_patterns)
              
              
            print("-------------")
            df_all_patterns = pd.DataFrame() 
            if len(df_patterns_list) > 0:
              df_all_patterns = pd.concat(df_patterns_list)
            
            if len(df_all_patterns) == 0 or df_all_patterns.shape[0] == 0:
              df_all_patterns = pd.DataFrame() 
            else:
              df_all_patterns = postprocessing_st_pattern_results(df_all_patterns, df_geonames_info)
              print(df_all_patterns)
            
            final_result_filename = "seasonal_periodic_st_motifs_" + result_filename_suffix + ".csv"
            out_pattern_results_filepath = os.path.join(output_result_folder, final_result_filename)
            df_all_patterns.to_csv(out_pattern_results_filepath, sep=";", quoting=csv.QUOTE_NONNUMERIC)
                  
              