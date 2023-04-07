'''
Created on Sep 16, 2022

@author: nejat
'''

import news_outlet_analysis.extract_fractional_counting_cascade_graph as cg
from util_event import read_df_events, read_events_from_df, get_event_clusters_from_clustering_result

from news_outlet_analysis.influence_maximization.run_influence_maximization_celf import runInfluenceMaximizationCelfForGeneric
from news_outlet_analysis.influence_maximization.extract_leskovec_cascade_graph import extractLeskovecCascadeGraphForGeneric

import os
import consts
import networkx as nx
import pandas as pd
import csv



def perform_news_outlet_time_detection_analysis(in_taxonomy_folder, in_news_websites_geo_folder, event_candidates_filepath, clustering_result_filepath, \
                                   output_dirpath, by_continent="-1"):
  df_event_candidates = read_df_events(event_candidates_filepath)
  event_candidates = read_events_from_df(df_event_candidates, in_taxonomy_folder)
  clusters = get_event_clusters_from_clustering_result(clustering_result_filepath, event_candidates)

  if by_continent != "-1" and by_continent in ["EU", "AS", "NA", "AF", "SA"]:
    event_candidates = [e for e in event_candidates if e.loc.get_continent() == by_continent]
    clusters_new = []
    for cluster in clusters:
      cluster_new = [e for e in cluster if e.loc.get_continent() == by_continent]
      if len(cluster_new)>0:
        clusters_new.append(cluster_new)
    clusters = clusters_new
    
    
  # PART 1
  graph_filename = "leskovec_time_detection_network.graphml"
  if by_continent != "-1":
    graph_filename = "leskovec_time_detection_network_continent="+by_continent+".graphml"
  graph_filepath = os.path.join(output_dirpath, graph_filename)
  extractLeskovecCascadeGraphForGeneric(event_candidates, clusters, graph_filepath)
    
  # PART 2
  det_time_result_filepath = os.path.join(output_dirpath, "leskovec_celf_detection_time" + "." + consts.FILE_FORMAT_CSV)
  if by_continent != "-1":
    det_time_result_filepath = os.path.join(output_dirpath, "leskovec_celf_detection_time_continent="+by_continent+"."+ consts.FILE_FORMAT_CSV)
  det_time_plot_filepath = os.path.join(output_dirpath, "leskovec_celf_detection_time" + "." + consts.FILE_FORMAT_PDF)
  if by_continent != "-1":
    det_time_plot_filepath = os.path.join(output_dirpath, "leskovec_celf_detection_time_continent="+by_continent+"."+ consts.FILE_FORMAT_PDF)

  k = 10
  runInfluenceMaximizationCelfForGeneric(in_news_websites_geo_folder, det_time_result_filepath, graph_filepath, det_time_plot_filepath, k)


    
    
    
def perform_news_outlet_pagerank_analysis(in_taxonomy_folder, event_candidates_filepath, clustering_result_filepath, \
                                   output_dirpath, by_continent="-1"):
  df_event_candidates = read_df_events(event_candidates_filepath)
  event_candidates = read_events_from_df(df_event_candidates, in_taxonomy_folder)
  clusters = get_event_clusters_from_clustering_result(clustering_result_filepath, event_candidates)

  if by_continent != "-1" and by_continent in ["EU", "AS", "NA", "AF", "SA"]:
    event_candidates = [e for e in event_candidates if e.loc.get_continent() == by_continent]
    clusters_new = []
    for cluster in clusters:
      cluster_new = [e for e in cluster if e.loc.get_continent() == by_continent]
      if len(cluster_new)>0:
        clusters_new.append(cluster_new)
    clusters = clusters_new
  
  graph_filename = "directed_newslet_cascade_network.graphml"
  if by_continent != "-1":
    graph_filename = "directed_newslet_cascade_network_continent="+by_continent+".graphml"
  cg.extractFractionalCountingCascadeGraph(event_candidates, clusters, output_dirpath, graph_filename)

  # read the resulting graph
  graph_filepath = os.path.join(output_dirpath, graph_filename)
  graph = nx.read_graphml(graph_filepath)
  
  # run the page rank algorithm
  print("nb nodes before removing isolated nodes:", graph.number_of_nodes())
  graph.remove_nodes_from(list(nx.isolates(graph)))
  print("nb nodes after removing isolated nodes:", graph.number_of_nodes())
  pr_dict = nx.pagerank(graph)
  node_ids = list(pr_dict.keys())
  pr_values = list(pr_dict.values())
  source_names = [graph.nodes[id]["name"] for id in node_ids]
  # print(pr_dict)
  
  # write the page rank results
  df_pr = pd.DataFrame({"id": node_ids, "pagerank_score": pr_values, "source_name": source_names})
  df_pr.sort_values(["pagerank_score"], ascending=[False], inplace=True)
  pr_filename = "newslet_pagerank_result.csv"
  if by_continent != "-1":
    pr_filename = "newslet_pagerank_result_continent="+by_continent+".csv"
  pr_filepath = os.path.join(output_dirpath, pr_filename)
  df_pr.to_csv(pr_filepath, index=False, sep=";", quoting=csv.QUOTE_NONNUMERIC)
  
  
  