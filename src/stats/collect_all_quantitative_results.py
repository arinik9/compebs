'''
Created on Apr 7, 2023

@author: nejat
'''

import pandas as pd
import numpy as np
import csv

from plot.plot_radar_chart import plot_radar_chart_from_df




def get_quantitative_eval_score(res_eval_filepath, column_name):
  df_result = pd.read_csv(res_eval_filepath, sep=";", keep_default_na=False)
  eval_spatial_mean_value = np.mean(df_result[column_name].to_numpy())
  return(eval_spatial_mean_value)


def retrieve_and_plot_all_quantitative_results(platforms, eval_filepath_dict, column_name_dict, csv_out_filepath, plot_output_filepath):
  res_dict = {}
  
  column_names = eval_filepath_dict[platforms[0]].keys()
  
  for platform_name in platforms:
    print("---", platform_name)
    res_dict[platform_name] = []
    
    for dim_name in eval_filepath_dict[platform_name].keys():
      print(dim_name)
      column_name = column_name_dict[platform_name][dim_name]
      eval_filepath = eval_filepath_dict[platform_name][dim_name]
      eval_mean_value = get_quantitative_eval_score(eval_filepath, column_name)
      res_dict[platform_name].append(eval_mean_value)
    
  
  df_final = pd.DataFrame.from_dict(res_dict, orient='index', columns = column_names).reset_index()
  df_final.rename(columns={"index": "group"}, inplace=True)
  print(df_final)
  csv_out_filepath
  df_final.to_csv(csv_out_filepath, sep=";", quoting=csv.QUOTE_NONNUMERIC, index=False)

  plot_radar_chart_from_df(df_final, plot_output_filepath)
  
  