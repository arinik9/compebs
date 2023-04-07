'''
Created on Nov 30, 2022

@author: nejat
'''


import os
import pandas as pd
import csv

from path import get_spatiotemporal_custom_folder_path
from stats.compute_rank_cor_news_outlets import compute_Kishida_normalized_precision, compute_Kishida_normalized_recall, compute_Kishida_normalized_fmeasure




def compute_Kishida_normalized_precision_and_recall_for_continuous_periodic_st_motifs(in_folder, out_folder, ref_platform, platforms, spatial_scales, temporal_scales):

  in_folder_platform = os.path.join(in_folder, "<PLATFORM>")
  out_folder_platform = os.path.join(out_folder, "<PLATFORM>")
  input_dirpath_platform = in_folder_platform
  
  minPS_values = [0.1] # 0.2, 0.3, 0.4, 0.5
  maxIAT_values = [2] # expressed in the selected temporal scale, e.g. 1 week
  tresh_distance_in_km_values = [1000]
  
  for platform in platforms:
    res_dict = {}
    
    for spatial_scale in spatial_scales:
      for temporal_scale in temporal_scales:
        print("platform:", platform, "temporal_scale:", temporal_scale)
        for tresh_distance_in_km in tresh_distance_in_km_values:
          for minPS in minPS_values:
            for maxIAT in maxIAT_values:  

              base_result_filename_suffix = "minPS="+str(minPS)+"_maxIAT="+str(maxIAT)+"_maxDist="+str(tresh_distance_in_km)
              result_filename_suffix = base_result_filename_suffix + "_platform="+platform
              
              input_folder = get_spatiotemporal_custom_folder_path(input_dirpath_platform, platform, \
                                                             spatial_scale=spatial_scale, temporal_scale=temporal_scale)
              pattern_filename = "continuous_periodic_st_motifs_" + result_filename_suffix + ".csv"
              result_filepath = os.path.join(input_folder, pattern_filename)
              df_patterns = pd.read_csv(result_filepath, sep=";", keep_default_na=False)
              df_patterns['solutions'] = df_patterns['Patterns'].astype("string").str.strip()
              
              input_folder = get_spatiotemporal_custom_folder_path(input_dirpath_platform, ref_platform, \
                                                             spatial_scale=spatial_scale, temporal_scale=temporal_scale)
              result_filename_suffix = base_result_filename_suffix + "_platform="+ref_platform
              ref_pattern_filename = "continuous_periodic_st_motifs_" + result_filename_suffix + ".csv"
              ref_result_filepath = os.path.join(input_folder, ref_pattern_filename)
              df_patterns_ref = pd.read_csv(ref_result_filepath, sep=";", keep_default_na=False)
              df_patterns_ref['solutions'] = df_patterns_ref['Patterns'].astype("string").str.strip()
              
              if df_patterns.shape[0]>0 and df_patterns_ref.shape[0]>0:
                precision_val, nb_common_patterns = compute_Kishida_normalized_precision(df_patterns_ref, df_patterns)
                recall_val, nb_common_patterns = compute_Kishida_normalized_recall(df_patterns_ref, df_patterns)
                fmeasure_val = compute_Kishida_normalized_fmeasure(df_patterns_ref, df_patterns)
                
                fmeasure_val = 0.0
                if recall_val>0 and precision_val>0:
                  fmeasure_val = 2*(recall_val*precision_val)/(recall_val+precision_val)
                print("for", platform, fmeasure_val) # recall_val, precision_val
                
                res_dict[result_filepath] = fmeasure_val #str(fmeasure_val)+" ("+str(nb_common_patterns)+")"
              else:
                res_dict[result_filepath] = 0.0 #str(0.0)+" ("+str(0)+")"
            
    # write into file
    output_folder = get_spatiotemporal_custom_folder_path(out_folder_platform, platform)
    df_comp = pd.DataFrame.from_dict(res_dict, orient='index', columns=["fmeasure"])
    res_rank_eval_filename = "rank_Kishida_normalized_fmeasure_for_continuous_periodic_st_motifs_"+platform+".csv"
    res_rank_eval_filepath = os.path.join(output_folder, res_rank_eval_filename)
    df_comp.to_csv(res_rank_eval_filepath, sep=";", quoting=csv.QUOTE_NONNUMERIC)
  
  
  
