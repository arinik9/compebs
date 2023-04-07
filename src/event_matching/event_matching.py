'''
Created on Jan 12, 2022

@author: nejat
'''


import os
import csv

from util_event import read_df_events, read_events_from_df
from event_matching.event_matching_strategy import EventMatchingStrategy, EventMatchingStrategyPossiblyDuplicate



class EventMatching():

  def __init__(self, event_matching_strategy:EventMatchingStrategy):
    self.event_matching_strategy = event_matching_strategy
    
        

  def perform_event_matching(self, in_taxonomy_folder, platform1_desc, platform1_events_filepath,\
                                        platform2_desc, platform2_events_filepath, output_dirpath):
    try:
      if not os.path.exists(output_dirpath):
        os.makedirs(output_dirpath)
    except OSError as err:
      print(err)
    
    df_events_platform1 = read_df_events(platform1_events_filepath)
    events_platform1 = read_events_from_df(df_events_platform1, in_taxonomy_folder)
    df_events_platform2 = read_df_events(platform2_events_filepath)
    events_platform2 = read_events_from_df(df_events_platform2, in_taxonomy_folder)
    
    # ===================================================================================
    # PERFORM EVENT MATCHING and store the result in output folder
    # ===================================================================================
    
    df_event_matching = self.event_matching_strategy.perform_event_matching(events_platform1, events_platform2)
    df_event_matching.rename(columns={'event1_id': platform1_desc+'_id', \
                                 'event1_loc_info': platform1_desc+'_loc_info', \
                                 'event1_loc_hierarchy': platform1_desc+'_loc_hierarchy', \
                                 'event1_date': platform1_desc+'_date',\
                                 'event1_disease': platform1_desc+'_disease',\
                                 'event1_host': platform1_desc+'_host',\
                                 'event2_id': platform2_desc+'_id', \
                                 'event2_loc_info': platform2_desc+'_loc_info', \
                                 'event2_loc_hierarchy': platform2_desc+'_loc_hierarchy', \
                                 'event2_date': platform2_desc+'_date',\
                                 'event2_disease': platform2_desc+'_disease',\
                                 'event2_host': platform2_desc+'_host',\
                                  }, inplace=True)
    
    
    # write into file
    result_filename = platform1_desc+"_"+platform2_desc+"_event_matching.csv"
    result_filepath = os.path.join(output_dirpath, result_filename)
    df_event_matching.to_csv(result_filepath, sep=";", quoting=csv.QUOTE_NONNUMERIC)
    
    
    
