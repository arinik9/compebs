'''
Created on Nov 29, 2022

@author: nejat
'''

import os
import pandas as pd
import numpy as np
import networkx as nx

from PAMI.partialPeriodicSpatialPattern.basic import STEclat


from util_event import read_df_events

import datetime

from datetime import timedelta
import dateutil.parser as parser

import itertools
from hin.create_heterogeneous_graph import create_heterogeneous_graph_from_events

import csv

from path import get_spatiotemporal_custom_folder_path



def get_date_diff_in_hours(date1, date2):
  time_difference = date2 - date1
  time_difference_in_hours = time_difference / timedelta(minutes=60)
  return int(time_difference_in_hours)


# it includes the node id and its up level values
def generate_all_up_hier_level_values(graph, node_id):
  up_list = [node_id]
  queue = [node_id]
  while len(queue)>0:
    curr_node_id = queue.pop(0)
    out_neighbors = graph.successors(curr_node_id)
    for neigh_id in out_neighbors:
      # graph.edges[curr_node_id,neigh_id]["type"] >> 3038375 {'weight': 3, 'type': 'down_hierarchy'}
      if graph.edges[curr_node_id,neigh_id]["type"] == "up_hierarchy":
        up_list.append(neigh_id)
        queue.append(neigh_id)
  #print("in:", node_id)
  #print("out:", up_list)
  return(up_list)




def create_event_hin_with_hierarchy(in_taxonomy_folder, df_events, out_graph_filepath, geonames_info_filepath):
  df = pd.read_csv(geonames_info_filepath, sep=";", keep_default_na=False)
  geonameId_to_name = dict(zip(df["geonames_id"], df["name"]))
  geonameId_to_lat = dict(zip(df["geonames_id"], df["lat"]))
  geonameId_to_lng = dict(zip(df["geonames_id"], df["lng"]))
  geonameId_to_hier_level = dict(zip(df["geonames_id"], df["hier_level"]))

  create_heterogeneous_graph_from_events(in_taxonomy_folder, df_events, out_graph_filepath, geonameId_to_name, \
                                          geonameId_to_lat, geonameId_to_lng, geonameId_to_hier_level)



def preprocessing_for_temporal_multidim_patterns(hin_graph, TDB_filepath, neighborhood_filepath, ref_begin_date):
  
  #STEP 1: create temporal database
  
  SEP = "\t"
  #print(ref_begin_date)
  #event_nodes = [(d[0], parser.parse(d[1]["date"])) for d in hin_graph.nodes(data=True) if d[1]["type"] == "event"]
  event_nodes = [(d[0], get_date_diff_in_hours(ref_begin_date, parser.parse(d[1]["date"]))) for d in hin_graph.nodes(data=True) if d[1]["type"] == "event"]
  event_nodes.sort(key = lambda x: x[1])
  
  unique_loc_ids = []
  lines_dict = {}
  for curr_event_node in event_nodes:
    event_id = curr_event_node[0]
    t = curr_event_node[1]
    line_content = ""
    
    loc_node_ids = [neigh_id for neigh_id in hin_graph.neighbors(event_id) if hin_graph.nodes[neigh_id]["type"] == "location"]
    host_node_ids = [neigh_id for neigh_id in hin_graph.neighbors(event_id) if hin_graph.nodes[neigh_id]["type"] == "host"]
    disease_node_ids = [neigh_id for neigh_id in hin_graph.neighbors(event_id) if hin_graph.nodes[neigh_id]["type"] == "disease"]
  
    for loc in loc_node_ids: # normally, we have 1 element here
      for host in host_node_ids:
        for disease in disease_node_ids: # normally, we have 1 element here
          loc_up_list = generate_all_up_hier_level_values(hin_graph, loc)
          unique_loc_ids = unique_loc_ids + loc_up_list
          host_up_list = generate_all_up_hier_level_values(hin_graph, host)
          disease_up_list = generate_all_up_hier_level_values(hin_graph, disease)
          for key in itertools.product(loc_up_list, disease_up_list, host_up_list):
            # a = [1, 2] and b = ["a", "b"]
            # (1, 'a')
            # (1, 'b')
            # (2, 'a')
            # (2, 'b')
            if line_content != "":
              line_content = line_content + SEP 
            line_content += "_".join(key)
    #
    unique_loc_ids = list(np.unique(unique_loc_ids))
    while t in lines_dict: # find the next available timestamp >> we want the timestamps to be distinct
      t += 1
    lines_dict[t] = line_content
    #file_lines.append(line_content)
  file_lines = []
  for key, value in lines_dict.items():
    file_lines.append(str(key)+SEP+value)
  file_content = "\n".join(file_lines)
  with open(TDB_filepath, 'w') as f:
    f.write(file_content)
    
  # STEP 2: crating neighborhood file for the STEclat algo
  #  since we do not use spatial info, the neighborhood file is useless
  unique_int_loc_ids = [int(loc_id) for loc_id in unique_loc_ids]
  unique_str_loc_ids = [str(loc_id) for loc_id in sorted(unique_int_loc_ids, reverse=False)]
  file_content = "\n".join(unique_str_loc_ids)
  with open(neighborhood_filepath, 'w') as f:
    f.write(file_content)
    
  return TDB_filepath, neighborhood_filepath
  



def extract_temporal_multidim_patterns(TDB_filepath, neighborhood_filepath, delta_days, output_filepath):
  ## source: https://github.com/udayRage/PAMI/blob/main/docs/partialPeriodicSpatialPatternMining.md
  minPS = 1
  maxIAT = delta_days # we can also assign a value by reading the last timestamp from TDB_filepath
  obj = STEclat.STEclat(TDB_filepath, neighborhood_filepath, minPS, maxIAT) # separator is '\t' by default
  obj.startMine() # this outputs: "Spatial Periodic Frequent patterns were generated successfully using SpatialEclat algorithm"
  partialPeriodicSpatialPatterns = obj.getPatterns()
  print("Total number of Periodic Spatial Frequent Patterns:", len(partialPeriodicSpatialPatterns))
  obj.save(output_filepath)
  df = obj.getPatternsAsDataFrame()     #Get the patterns discovered into a dataframe 
  return(df)
  
  
def postprocessing_temporal_multidim_pattern_results(df_patterns, df_geonames_info, df_disease_info, df_host_info):
  # df_patterns has 2 columns: "Patterns", "periodicSupport"
  
  # location
  geonameId_to_name = dict(zip(df_geonames_info["geonames_id"], df_geonames_info["name"]))
  geonameId_to_country_id = dict(zip(df_geonames_info["geonames_id"], df_geonames_info["country_id"]))
  geonameId_to_country_code = dict(zip(df_geonames_info["geonames_id"], df_geonames_info["country_code"]))
  geonameId_to_hier_level = dict(zip(df_geonames_info["geonames_id"], df_geonames_info["hier_level"]))
  geonameId_to_lat = dict(zip(df_geonames_info["geonames_id"], df_geonames_info["lat"]))
  geonameId_to_lng = dict(zip(df_geonames_info["geonames_id"], df_geonames_info["lng"]))
  # disease
  disease_text_to_disease = dict(zip(df_disease_info["text"], df_disease_info["disease"]))
  disease_text_to_hier_level = dict(zip(df_disease_info["text"], df_disease_info["hier_level"]))
  # host
  host_text_to_host = dict(zip(df_host_info["text"], df_host_info["host"]))
  host_text_to_hier_level = dict(zip(df_host_info["text"], df_host_info["hier_level"]))
  
  df_patterns["geonames_id"] = df_patterns["Patterns"].apply(lambda x: int(x.split("_")[0]))
  df_patterns["freq"] = df_patterns["periodicSupport"]
  df_patterns["country_id"] = df_patterns["geonames_id"].apply(lambda x: geonameId_to_country_id[x])
  df_patterns["country_code"] = df_patterns["geonames_id"].apply(lambda x: geonameId_to_country_code[x])
  df_patterns["loc_hier_level"] = df_patterns["geonames_id"].apply(lambda x: geonameId_to_hier_level[x])
  
  df_country_freqs = df_patterns.groupby('country_id').apply(lambda group: group['freq'].max())
  country_id_to_freq = dict(zip(df_country_freqs.index, df_country_freqs.to_list()))
  df_patterns["country_freq"] = df_patterns["country_id"].apply(lambda x: country_id_to_freq[x])
  
  df_patterns["disease_text"] = df_patterns["Patterns"].apply(lambda x: x.split("_")[1].strip())
  df_patterns["disease"] = df_patterns["disease_text"].apply(lambda x: disease_text_to_disease[x])
  df_patterns["disease_hier_level"] = df_patterns["disease_text"].apply(lambda x: disease_text_to_hier_level[x])
  
  df_patterns["host_text"] = df_patterns["Patterns"].apply(lambda x: x.split("_")[2].strip())
  df_patterns["host"] = df_patterns["host_text"].apply(lambda x: host_text_to_host[x])
  df_patterns["host_hier_level"] = df_patterns["host_text"].apply(lambda x: host_text_to_hier_level[x])
                                                      
  #df_patterns.sort_values(['country_freq', 'loc_hier_level', 'geonames_id', 'disease_hier_level', 'host_hier_level'], ascending=[False, True, True, True, True], inplace=True)
  df_patterns.sort_values(['freq'], ascending=[False], inplace=True)

  df_patterns.pop("Patterns")
  df_patterns.pop("periodicSupport")
  df_patterns.pop("country_freq")
  return(df_patterns)





def process_continuous_periodic_multidim_st_motif_extraction(in_folder, in_taxonomy_folder, out_folder, platform_name, out_preprocessing_folder, continents, periods, seasons):
  
  out_folder_platform = os.path.join(out_folder, "<PLATFORM>")
  output_dirpath_platform = out_folder_platform
  
  # we multiply delay time with 24 because, the delay is expressed in hours for practical reasons in STEclat algo
  for analysis_settings in [("static", 100000000), ("temporal", 10*24), ("temporal", 30*24), ("temporal", 60*24), ("temporal", 90*24)]:
    analysis_type = analysis_settings[0]
    delta_days = analysis_settings[1]
    for continent_name in continents:
      for season in seasons:
        for year in periods:  
          output_result_folder = get_spatiotemporal_custom_folder_path(output_dirpath_platform, platform_name, continent_name, season, year)
          print(output_result_folder)
          
          result_filename_suffix = "type="+analysis_type
          if analysis_type == "temporal":
            result_filename_suffix += "_window="+str(delta_days)
          result_filename_suffix += "_platform="+platform_name
          
          try:
            if not os.path.exists(output_result_folder):
              os.makedirs(output_result_folder)
          except OSError as err:
            print(err)
            
          input_folder = os.path.join(in_folder, platform_name)
          events_filepath = os.path.join(input_folder, "events.csv")
          df_events = read_df_events(events_filepath)
          
          # ============================
          # Filter
          if year != "":
            df_events = df_events[df_events["year"] == year]
          if season != "":
            df_events = df_events[df_events["season"] == season]
          if continent_name != "":
            df_events = df_events[df_events["continent"] == continent_name]
          print("nb:", df_events.shape)
          # ============================

          year_values = np.unique(df_events["year"].sort_values(ascending=True).to_list())
          ref_begin_date = datetime.datetime(year_values[0], 1, 1, 0, 0, 0)
          
          geonames_info_filepath = os.path.join(out_preprocessing_folder, "geonames_info.csv")
          df_geonames_info = pd.read_csv(geonames_info_filepath, sep=";", keep_default_na=False)
          geonameId_to_name = dict(zip(df_geonames_info["geonames_id"], df_geonames_info["name"]))
          
          disease_info_filepath = os.path.join(in_taxonomy_folder, "disease_info.csv")
          df_disease_info = pd.read_csv(disease_info_filepath, sep=";", keep_default_na=False)
          
          host_info_filepath = os.path.join(in_taxonomy_folder, "host_info.csv")
          df_host_info = pd.read_csv(host_info_filepath, sep=";", keep_default_na=False)
          
          graph_filename = "event_hin_" + result_filename_suffix + ".graphml"
          graph_filepath = os.path.join(output_result_folder, graph_filename)
          create_event_hin_with_hierarchy(in_taxonomy_folder, df_events, graph_filepath, geonames_info_filepath)
          hin_graph = nx.read_graphml(graph_filepath)
          print("n: ", hin_graph.number_of_nodes(), ", m: ", hin_graph.number_of_edges())

          TDB_filepath = os.path.join(output_result_folder, "TDB.txt")
          neighborhood_filepath = os.path.join(output_result_folder, "neighborhood.txt")
          preprocessing_for_temporal_multidim_patterns(hin_graph, TDB_filepath, neighborhood_filepath, ref_begin_date)
          
          raw_result_filename = "raw_continuous_periodic_st_multidim_motifs_" + result_filename_suffix + ".txt"
          output_filepath = os.path.join(output_result_folder, raw_result_filename)
          df_patterns = extract_temporal_multidim_patterns(TDB_filepath, neighborhood_filepath, delta_days, output_filepath)
          print(df_patterns)
          print("-------------")
          
          if len(df_patterns) == 0 or df_patterns.shape[0] == 0:
            df_patterns = pd.DataFrame() 
          else:
            df_patterns = postprocessing_temporal_multidim_pattern_results(df_patterns, df_geonames_info, df_disease_info, df_host_info)
            print(df_patterns)
          
          final_result_filename = "continuous_periodic_st_multidim_motifs_" + result_filename_suffix + ".csv"
          out_pattern_results_filepath = os.path.join(output_result_folder, final_result_filename)
          df_patterns.to_csv(out_pattern_results_filepath, sep=";", quoting=csv.QUOTE_NONNUMERIC)
          
            
