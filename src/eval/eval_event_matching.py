'''
Created on Apr 7, 2023

@author: nejat
'''


import pandas as pd
import numpy as np
import csv



def eval_event_matching_with_ground_truth(platform1_name, ref_platform_name, 
                                          platform1_id_to_ref_platform_dict, event_matching_result_filepath, 
                                          platform1_id_to_article_id, article_id_to_platform1_id,
                                          out_eval_event_matching_filepath,  out_eval_score_filepath):
  
  platform1_id_column_name = platform1_name+"_id"
  ref_platform_id_column_name = ref_platform_name+"_id"
  column_names = [platform1_id_column_name, ref_platform_id_column_name]
  df_event_matching_result = pd.read_csv(event_matching_result_filepath, sep=";", keep_default_na=False, usecols=column_names)

  
  correct_ref_id_list = []
  eval_status_list = []
  for index, row in df_event_matching_result.iterrows():
    id_for_platform1 = row[platform1_id_column_name]
    article_ids_for_platform1 = platform1_id_to_article_id[id_for_platform1] # it returns multiple article ids
    # we suppose that all these articles report the same event, so take the first one
    article_id_for_platform1 = int(article_ids_for_platform1[0].split("-")[1]) # "2-123414" (event id - article id) >> split by "-" and take the 2nd part
    
    id_for_ref_platform_after_event_matching = row[ref_platform_id_column_name]
    ground_truth_ref_id = platform1_id_to_ref_platform_dict[article_id_for_platform1]
    
    correct_ref_id_list.append(ground_truth_ref_id)
    
    if id_for_ref_platform_after_event_matching == ground_truth_ref_id:
      eval_status_list.append(1) # success
    else:
      eval_status_list.append(0) # failure
      
  df_event_matching_result["eval_status"] = eval_status_list
  df_event_matching_result["correct_"+ref_platform_id_column_name] = correct_ref_id_list
  df_event_matching_result[platform1_name+"_article_id"] = df_event_matching_result[platform1_id_column_name].apply(lambda x: str(platform1_id_to_article_id[x]))
  df_event_matching_result.to_csv(out_eval_event_matching_filepath, sep=";", quoting=csv.QUOTE_NONNUMERIC, index=False)
  
  mean_eval_value = np.mean(eval_status_list)
  df_eval_score = pd.DataFrame.from_dict({"score": [mean_eval_value]})
  df_eval_score.to_csv(out_eval_score_filepath, sep=";", quoting=csv.QUOTE_NONNUMERIC, index=False)

  print(mean_eval_value)
  
  