'''
Created on Nov 30, 2022

@author: nejat
'''


import os
import pandas as pd
import csv

from stats.compute_rank_cor_news_outlets import compute_Kishida_normalized_precision, compute_Kishida_normalized_recall, compute_Kishida_normalized_fmeasure
from path import get_spatiotemporal_custom_folder_path




def compute_Kishida_normalized_precision_and_recall_for_multidim_motifs(in_folder, out_folder, ref_platform, platforms, continents, periods, seasons):
  
  in_folder_platform = os.path.join(in_folder, "<PLATFORM>")
  out_folder_platform = os.path.join(out_folder, "<PLATFORM>")
  input_dirpath_platform = in_folder_platform
  
  
  for platform in platforms:
    res_dict = {}
    
    # we multiply delay time with 24 because, the delay is expressed in hours for practical reasons in STEclat algo
    for analysis_settings in [("static", 100000000), ("temporal", 10*24), ("temporal", 30*24), ("temporal", 60*24), ("temporal", 90*24)]:
      analysis_type = analysis_settings[0]
      print("platform:", platform, "with", analysis_settings)
      delta_days = analysis_settings[1]
      for continent_name in continents:
        for season in seasons:
          for year in periods:  

            base_result_filename_suffix = "type="+analysis_type
            if analysis_type == "temporal":
              base_result_filename_suffix += "_window="+str(delta_days)
            
            result_filename_suffix = base_result_filename_suffix + "_platform="+platform
            input_folder = get_spatiotemporal_custom_folder_path(input_dirpath_platform, platform, continent_name, season, year)
            pattern_filename = "continuous_periodic_st_multidim_motifs_" + result_filename_suffix + ".csv"
            result_filepath = os.path.join(input_folder, pattern_filename)
            df_patterns = pd.read_csv(result_filepath, sep=";", keep_default_na=False)
            columns = ["geonames_id", "disease_text", "host_text"]
            df_patterns['solutions'] = df_patterns[columns].apply(lambda row: '_'.join(row.values.astype(str)), axis=1) # Kishida normalized stats requires this column name
            
            input_folder = get_spatiotemporal_custom_folder_path(input_dirpath_platform, ref_platform, continent_name, season, year)
            result_filename_suffix = base_result_filename_suffix + "_platform="+ref_platform
            ref_pattern_filename = "continuous_periodic_st_multidim_motifs_" + result_filename_suffix + ".csv"
            ref_result_filepath = os.path.join(input_folder, ref_pattern_filename)
            df_patterns_ref = pd.read_csv(ref_result_filepath, sep=";", keep_default_na=False)
            columns = ["geonames_id", "disease_text", "host_text"]
            df_patterns_ref['solutions'] = df_patterns_ref[columns].apply(lambda row: '_'.join(row.values.astype(str)), axis=1) # Kishida normalized stats requires this column name
            
            if df_patterns.shape[0]>0 and df_patterns_ref.shape[0]>0:
              precision_val, nb_common_patterns = compute_Kishida_normalized_precision(df_patterns_ref, df_patterns)
              recall_val, nb_common_patterns = compute_Kishida_normalized_recall(df_patterns_ref, df_patterns)
              fmeasure_val = compute_Kishida_normalized_fmeasure(df_patterns_ref, df_patterns)
                
              print("for", platform, fmeasure_val) # recall_val, precision_val
              
              res_dict[result_filepath] = fmeasure_val #str(fmeasure_val)+" ("+str(nb_common_patterns)+")"
            else:
              res_dict[result_filepath] = 0.0 #str(0.0)+" ("+str(0)+")"
            
    # write into file
    output_folder = get_spatiotemporal_custom_folder_path(out_folder_platform, platform)
    df_comp = pd.DataFrame.from_dict(res_dict, orient='index', columns=["fmeasure"])
    #res_rank_corr_filename = "rank_corr_for_multidim_motifs.csv"
    res_rank_eval_filename = "rank_Kishida_normalized_fmeasure_for_continuous_periodic_st_multidim_motifs_"+platform+".csv"
    res_rank_eval_filepath = os.path.join(output_folder, res_rank_eval_filename)
    df_comp.to_csv(res_rank_eval_filepath, sep=";", quoting=csv.QUOTE_NONNUMERIC)
  
  