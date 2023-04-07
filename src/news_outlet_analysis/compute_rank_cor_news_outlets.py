'''
Created on Nov 30, 2022

@author: nejat
'''


import os
import pandas as pd
import csv

from stats.compute_rank_cor_news_outlets import compute_Kishida_normalized_precision, compute_Kishida_normalized_recall, compute_Kishida_normalized_fmeasure




def compute_Kishida_normalized_precision_and_recall_for_news_outlets(in_folder, out_folder, platforms, by_continent_values):
  LIMIT = 30

  desc_list = []
  precision_val_list = []
  recall_val_list = []
  fmeasure_val_list = []
  nb_common_patterns_list = []
  
  for platform_name in platforms:
    res_dict = {}
    
    for by_continent in by_continent_values:
      desc = "platform="+platform_name+"_by_continent="+by_continent
      
      input_folder = os.path.join(in_folder, platform_name)
      result_filepath = os.path.join(input_folder, "newslet_pagerank_result.csv")
      if by_continent != "-1":
        result_filepath = os.path.join(input_folder, "newslet_pagerank_result_continent="+by_continent+".csv")
      df_patterns = pd.read_csv(result_filepath, sep=";", keep_default_na=False)
      df_patterns['solutions'] = df_patterns['source_name'] # Kishida normalized stats requires this column name
              
      ref_result_filepath = os.path.join(input_folder, "leskovec_celf_detection_time.csv")
      if by_continent != "-1":
        ref_result_filepath = os.path.join(input_folder, "leskovec_celf_detection_time_continent="+by_continent+".csv")
      df_patterns_ref = pd.read_csv(ref_result_filepath, sep=";", keep_default_na=False)
      
      precision_val, nb_common_patterns = compute_Kishida_normalized_precision(df_patterns_ref, df_patterns, LIMIT)
      recall_val, nb_common_patterns = compute_Kishida_normalized_recall(df_patterns_ref, df_patterns, LIMIT)
      fmeasure_val = compute_Kishida_normalized_fmeasure(df_patterns_ref, df_patterns, LIMIT)
      
      # desc_list.append(desc)
      # precision_val_list.append(precision_val)
      # recall_val_list.append(recall_val)
      # fmeasure_val_list.append(fmeasure_val)
      # nb_common_patterns_list.append(nb_common_patterns)
      
      res_dict[result_filepath] = fmeasure_val


    output_folder = os.path.join(out_folder, platform_name)
    df_all = pd.DataFrame.from_dict(res_dict, orient='index', columns=["fmeasure"])
    res_eval_filename = "rank_Kishida_normalized_fmeasure_for_news_outlets_"+platform_name+".csv"
    res_eval_filepath = os.path.join(output_folder, res_eval_filename)
    df_all.to_csv(res_eval_filepath, sep=";", quoting=csv.QUOTE_NONNUMERIC)   
    

  