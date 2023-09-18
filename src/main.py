import os
import consts


from event_matching.event_matching import EventMatching
from event_matching.event_matching_strategy import EventMatchingStrategyEventSimilarity
from util_event import simplify_df_events_at_hier_level1

from event_matching.event_db_fusion import EventFusion
from event_matching.event_fusion_strategy import EventFusionStrategyMaxOccurrence
from itertools import combinations 








FORCE = False # TODO: use it systematically in every main function


if __name__ == '__main__':
  
  platforms_desc_list = []
  platforms_filepath_dict = {}
    
  #########################################
  # WAHIS
  #########################################
  input_event_folder_wahis = os.path.join(consts.IN_EVENTS_FOLDER, consts.NEWS_DB_WAHIS)
  events_filepath_empresi = os.path.join(input_event_folder_wahis, "corpus_events_wahis_task1=max-occurrence.csv")
     
  events_simplified_filepath_empresi = os.path.join(input_event_folder_wahis, "events_simplified.csv") # for DEBUG
  simplify_df_events_at_hier_level1(events_filepath_empresi, events_simplified_filepath_empresi) # for DEBUG
     
  platforms_desc_list.append(consts.NEWS_DB_WAHIS)
  platforms_filepath_dict[consts.NEWS_DB_WAHIS] = events_filepath_empresi
  

  #########################################
  # APHIS
  #########################################
  input_event_folder_aphis = os.path.join(consts.IN_EVENTS_FOLDER, consts.NEWS_DB_USA_APHIS)
  events_filepath_aphis = os.path.join(input_event_folder_aphis, "corpus_events_aphis_task1=max-occurrence.csv")
     
  events_simplified_filepath_aphis = os.path.join(input_event_folder_aphis, "events_simplified.csv") # for DEBUG
  simplify_df_events_at_hier_level1(events_filepath_aphis, events_simplified_filepath_aphis) # for DEBUG
     
  platforms_desc_list.append(consts.NEWS_DB_USA_APHIS)
  platforms_filepath_dict[consts.NEWS_DB_USA_APHIS] = events_filepath_aphis
  
  
  #########################################
  # APHA
  #########################################
  input_event_folder_apha = os.path.join(consts.IN_EVENTS_FOLDER, consts.NEWS_DB_UK_APHA)
  events_filepath_apha = os.path.join(input_event_folder_apha, "corpus_events_apha_task1=max-occurrence.csv")
     
  events_simplified_filepath_apha = os.path.join(input_event_folder_apha, "events_simplified.csv") # for DEBUG
  simplify_df_events_at_hier_level1(events_filepath_apha, events_simplified_filepath_apha) # for DEBUG
     
  platforms_desc_list.append(consts.NEWS_DB_UK_APHA)
  platforms_filepath_dict[consts.NEWS_DB_UK_APHA] = events_filepath_apha
  
  
  #########################################
  # PADI-Web
  #########################################
  input_event_folder_padiweb = os.path.join(consts.IN_EVENTS_FOLDER, consts.NEWS_SURVEILLANCE_PADIWEB)
  events_filepath_padiweb = os.path.join(input_event_folder_padiweb, "corpus_events_padiweb_task1=max-occurrence.csv")
  
  events_simplified_filepath_padiweb = os.path.join(input_event_folder_padiweb, "events_simplified.csv") # for DEBUG
  simplify_df_events_at_hier_level1(events_filepath_padiweb, events_simplified_filepath_padiweb) # for DEBUG
  
  platforms_desc_list.append(consts.NEWS_SURVEILLANCE_PADIWEB)
  platforms_filepath_dict[consts.NEWS_SURVEILLANCE_PADIWEB] = events_filepath_padiweb  
  
  #########################################
  # ProMED
  #########################################
  input_event_folder_promed = os.path.join(consts.IN_EVENTS_FOLDER, consts.NEWS_SURVEILLANCE_PROMED)
  events_filepath_promed = os.path.join(input_event_folder_promed, "corpus_events_promed_task1=max-occurrence.csv")
  
  events_simplified_filepath_promed = os.path.join(input_event_folder_promed, "events_simplified.csv") # for DEBUG
  simplify_df_events_at_hier_level1(events_filepath_promed, events_simplified_filepath_promed) # for DEBUG

  platforms_desc_list.append(consts.NEWS_SURVEILLANCE_PROMED)
  platforms_filepath_dict[consts.NEWS_SURVEILLANCE_PROMED] = events_filepath_promed    
  
    
 
  
  #########################################
  # EVENT MATCHING
  #
  # Event matching between all the considered EBS platforms pair by pair
  #  1) PADI-Web - ProMED, 2) PADI-Web - WAHIS, 3) ProMED - WAHIS, etc.
  #########################################
  output_dirpath_event_matching = os.path.join(consts.OUT_FOLDER, "event_matching")
  try:
    if not os.path.exists(output_dirpath_event_matching):
      os.makedirs(output_dirpath_event_matching)
  except OSError as err:
    print(err) 

  
  for platform_pair in list(combinations(platforms_desc_list, 2)):
    platform1_desc = platform_pair[0]
    platform2_desc = platform_pair[1]
  
    platform1_events_filepath = platforms_filepath_dict[platform1_desc]
    platform2_events_filepath = platforms_filepath_dict[platform2_desc]
  
    event_matching_strategy = EventMatchingStrategyEventSimilarity()
    job_event_matching = EventMatching(event_matching_strategy)
    job_event_matching.perform_event_matching(platform1_desc,\
                                              platform1_events_filepath,\
                                              platform2_desc,\
                                              platform2_events_filepath,\
                                              output_dirpath_event_matching)
  
  
  #########################################
  # EVENT FUSION
  ######################################### 

  output_dirpath_event_fusion = os.path.join(consts.OUT_FOLDER, "event_fusion")
  try:
    if not os.path.exists(output_dirpath_event_fusion):
      os.makedirs(output_dirpath_event_fusion)
  except OSError as err:
    print(err)
  
  
  event_fusion_strategy = EventFusionStrategyMaxOccurrence()
  event_fusion = EventFusion(event_fusion_strategy)
  print(platforms_desc_list)
  event_fusion.perform_event_db_fusion(output_dirpath_event_matching, output_dirpath_event_fusion, \
                                       platforms_desc_list, platforms_filepath_dict)
  
    
  
  
  