'''
Created on Nov 30, 2022

@author: nejat
'''

import os
import pandas as pd
import numpy as np
import csv

from path import get_spatiotemporal_custom_folder_path


def compute_temporal_geo_coverage(df_patterns_ref, df_patterns_cand):
  
  res_dict = {}
  
  df_patterns_ref["nb_items"] = df_patterns_ref["patternsDesc"].apply(lambda x: x.count(") ")+1)
  df_patterns_cand["nb_items"] = df_patterns_cand["patternsDesc"].apply(lambda x: x.count(") ")+1)
  
  df_1patterns_ref = df_patterns_ref[df_patterns_ref["nb_items"] == 1]
  df_1patterns_cand = df_patterns_cand[df_patterns_cand["nb_items"] == 1]
  df_1patterns_ref.sort_values(['patternsDesc', 'month_no'], ascending=[True,True], inplace=True)
  df_1patterns_cand.sort_values(['patternsDesc', 'month_no'], ascending=[True,True], inplace=True)
  
  unique_ref_country_list = np.unique(df_1patterns_ref["patternsDesc"].to_numpy())
  for country_id in unique_ref_country_list:
    df_sub_ref = df_1patterns_ref[df_1patterns_ref["patternsDesc"] == country_id]
    df_sub_cand = df_1patterns_cand[df_1patterns_cand["patternsDesc"] == country_id]
    
    res = 0.0
    if df_sub_cand.shape[0]>0:
      month_no_ref_vals = df_sub_ref["month_no"].to_list()
      month_no_cand_vals = df_sub_cand["month_no"].to_list()
      
      for month_no_ref_val in month_no_ref_vals:
        before = month_no_ref_val-1
        if month_no_ref_val == 1:
          before = 12
        after = month_no_ref_val+1
        if month_no_ref_val == 12:
          after = 1
          
        if (month_no_ref_val in month_no_cand_vals):
          res += 1
        elif (before in month_no_cand_vals):
          res += 1
        elif (after in month_no_cand_vals):
          res += 1
      res = res/len(month_no_ref_vals)
  
    res_dict[country_id] = res
    
  df_res = pd.DataFrame.from_dict(res_dict, orient='index', columns=['score'])
  #print(df_res)
  avg_val = np.mean(df_res["score"].to_numpy())
  return avg_val




def compute_temporal_geo_coverage_for_st_seasonal_periodic_motifs(in_folder, out_folder, ref_platform, platforms, spatial_scales, temporal_scales):
  
  in_folder_platform = os.path.join(in_folder, "<PLATFORM>")
  out_folder_platform = os.path.join(out_folder, "<PLATFORM>")
  input_dirpath_platform = in_folder_platform
  
  minPS_values = [0.5, 1.0]
  tresh_distance_in_km_values = [1000]
  
  for platform in platforms:
    res_dict = {}

    for spatial_scale in spatial_scales:
      for temporal_scale in temporal_scales:
        for minPS in minPS_values:
          for tresh_distance_in_km in tresh_distance_in_km_values:

            base_result_filename_suffix = "minPS="+str(minPS)+"_maxDist="+str(tresh_distance_in_km)
            result_filename_suffix = base_result_filename_suffix + "_platform="+platform
            
            input_folder = get_spatiotemporal_custom_folder_path(input_dirpath_platform, platform, \
                                                           spatial_scale=spatial_scale, temporal_scale=temporal_scale)
            pattern_filename = "seasonal_periodic_st_motifs_" + result_filename_suffix + ".csv"
            result_filepath = os.path.join(input_folder, pattern_filename)
            df_patterns = pd.read_csv(result_filepath, sep=";", keep_default_na=False)
            #print(result_filepath)
            
            input_folder = get_spatiotemporal_custom_folder_path(input_dirpath_platform, ref_platform, \
                                                           spatial_scale=spatial_scale, temporal_scale=temporal_scale)
            result_filename_suffix = base_result_filename_suffix + "_platform="+ref_platform
            ref_pattern_filename = "seasonal_periodic_st_motifs_" + result_filename_suffix + ".csv"
            ref_result_filepath = os.path.join(input_folder, ref_pattern_filename)
            df_patterns_ref = pd.read_csv(ref_result_filepath, sep=";", keep_default_na=False)
            #print(ref_result_filepath)
            
            if df_patterns.shape[0]>0 and df_patterns_ref.shape[0]>0:
              eval_val = compute_temporal_geo_coverage(df_patterns_ref, df_patterns)
              res_dict[result_filepath] = eval_val
            else:
              res_dict[result_filepath] = 0
              
            print("for", platform, "eval val:", eval_val)
            
    # write into file
    output_folder = get_spatiotemporal_custom_folder_path(out_folder_platform, platform)
    df_comp = pd.DataFrame.from_dict(res_dict, orient='index', columns=["temporal_geocoverage"])
    res_eval_filename = "temporal_geocoverage_for_seasonal_periodic_st_motifs_"+platform+".csv"
    res_eval_filepath = os.path.join(output_folder, res_eval_filename)
    df_comp.to_csv(res_eval_filepath, sep=";", quoting=csv.QUOTE_NONNUMERIC)
  
  