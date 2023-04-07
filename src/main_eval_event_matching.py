'''
Created on Dec 3, 2022

@author: nejat
'''

import os
import consts
import pandas as pd

from util_event import simplify_df_events_at_hier_level1, read_df_events
from event_matching.event_matching import EventMatching
from event_matching.event_matching_strategy import EventMatchingStrategyEventSimilarity
from eval.eval_event_matching import eval_event_matching_with_ground_truth



# ====================================================================
MAIN_FOLDER = "/home/nejat/eclipse/github/compebs"

IN_FOLDER = os.path.join(MAIN_FOLDER, "in-bahdja")
OUT_FOLDER = os.path.join(MAIN_FOLDER, "out-bahdja")

LIB_FOLDER = os.path.join(MAIN_FOLDER, "lib")
DATA_FOLDER = os.path.join(MAIN_FOLDER, "data")
# ====================================================================


IN_EVENTS_FOLDER = os.path.join(IN_FOLDER, "events")
IN_THEMATIC_TAXONOMY_FOLDER = os.path.join(IN_FOLDER, "thematic_taxonomy")




if __name__ == '__main__':
  
        
  #########################################
  # EMPRES-i
  #########################################
  input_event_folder_empres_i = os.path.join(IN_EVENTS_FOLDER, consts.NEWS_DB_EMPRESS_I)

  events_filepath_empresi = os.path.join(input_event_folder_empres_i, "events.csv")
     
  events_simplified_filepath_empresi = os.path.join(input_event_folder_empres_i, "events_simplified.csv")
  simplify_df_events_at_hier_level1(events_filepath_empresi, events_simplified_filepath_empresi)
     
      
  #########################################
  # PADI-Web
  #########################################
  input_event_folder_padiweb = os.path.join(IN_EVENTS_FOLDER, consts.NEWS_SURVEILLANCE_PADIWEB)
  
  event_candidates_filepath_padiweb = os.path.join(input_event_folder_padiweb, "event_candidates.csv")
  clustering_result_filepath_padiweb = os.path.join(input_event_folder_padiweb, "event-clustering.txt")
  events_filepath_padiweb = os.path.join(input_event_folder_padiweb, "events.csv")
     
  events_simplified_filepath_padiweb = os.path.join(input_event_folder_padiweb, "events_simplified.csv")
  simplify_df_events_at_hier_level1(events_filepath_padiweb, events_simplified_filepath_padiweb)
  
  
  
  #########################################
  # Event matching between the considered EBS platforms
  #  1) PADI-Web - ProMED, 2) PADI-Web - EMPRES-i, 3) ProMED - EMPRES-i
  #########################################
  output_dirpath_event_matching = os.path.join(OUT_FOLDER, "event_matching")
  try:
    if not os.path.exists(output_dirpath_event_matching):
      os.makedirs(output_dirpath_event_matching)
  except OSError as err:
    print(err)

  event_matching_strategy = EventMatchingStrategyEventSimilarity()
  job_event_matching = EventMatching(event_matching_strategy)  
  job_event_matching.perform_event_matching(IN_THEMATIC_TAXONOMY_FOLDER, consts.NEWS_SURVEILLANCE_PADIWEB,\
                                            events_filepath_padiweb,\
                                            consts.NEWS_DB_EMPRESS_I,\
                                            events_filepath_empresi,\
                                            output_dirpath_event_matching)
  
  
  
  
  #########################################
  # EVAL EVENT MATCHING
  #########################################
  
  df_events_padiweb = read_df_events(events_filepath_padiweb)
  
  padiweb_id_to_article_id = {}
  article_id_to_padiweb_id = {}
  for index, row in df_events_padiweb.iterrows():
    padiweb_id_to_article_id[row[consts.COL_ID]] = eval(row[consts.COL_ARTICLE_ID])
    for article_id in eval(row[consts.COL_ARTICLE_ID]):
      article_id_to_padiweb_id[article_id] = row[consts.COL_ID]
  
  ground_truth_filepath = os.path.join(IN_EVENTS_FOLDER, "ground_truth_event_matching", "articlesweb.csv")
  df_ground_truth = pd.read_csv(ground_truth_filepath, sep=";", keep_default_na=False, usecols=["alert_id", "Empres-i ref"])
  df_ground_truth.rename(columns={"alert_id": "id", "Empres-i ref": "id_ref"}, inplace=True)
  padiweb_id_to_empresi_id_dict = dict(zip(df_ground_truth["id"], df_ground_truth["id_ref"]))
  
  out_eval_event_mathing_folder = os.path.join(OUT_FOLDER, "eval-event-matching")
  try:
    if not os.path.exists(out_eval_event_mathing_folder):
      os.makedirs(out_eval_event_mathing_folder)
  except OSError as err:
    print(err)
    
  out_eval_event_matching_filepath = os.path.join(out_eval_event_mathing_folder, "result.csv")
  out_eval_score_filepath = os.path.join(out_eval_event_mathing_folder, "score.csv")
   
  
  event_matching_result_filename = consts.NEWS_SURVEILLANCE_PADIWEB+"_"+consts.NEWS_DB_EMPRESS_I+"_event_matching.csv"
  event_matching_result_filepath = os.path.join(output_dirpath_event_matching, event_matching_result_filename)
    
  eval_event_matching_with_ground_truth(consts.NEWS_SURVEILLANCE_PADIWEB, consts.NEWS_DB_EMPRESS_I, 
                                        padiweb_id_to_empresi_id_dict, event_matching_result_filepath,
                                        padiweb_id_to_article_id, article_id_to_padiweb_id,
                                         out_eval_event_matching_filepath, out_eval_score_filepath)

