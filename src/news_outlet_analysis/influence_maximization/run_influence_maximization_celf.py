'''
Created on Dec 9, 2021

@author: nejat
'''

# TODO
# https://arxiv.org/pdf/2008.02216.pdf: Fuzzy Jaccard Index: A robust comparison of ordered lists
# https://github.com/Petkomat/fuji-score

import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

from news_outlet_analysis.influence_maximization.outbreak_detection import celf_detection_time
from news_outlet_analysis.influence_maximization.news_source_geo_coverage import create_dict_url_to_pub_country_code, trim_url_custom2

# source: https://hautahi.com/ic_comparison


def plot_celf_results(df, plot_filepath, title, source_url_to_pub_country_code):
  x_values = list(df.index)
  y_values = df["penalty_reductions"]
  labels = df["solutions"]
  ext_labels = []
  for label in labels:
    source = trim_url_custom2(label)
    #most_similar_url = find_most_similar_url(label, source_url_to_pub_country_code)
    if source in source_url_to_pub_country_code:
      ext_labels.append(source+" ("+source_url_to_pub_country_code[source]+")")
    else:
      ext_labels.append(label)
      
  fig, ax = plt.subplots()
  ax.plot(x_values, y_values, linestyle = "solid")
  ax.scatter(x_values, y_values)
  for i, txt in enumerate(ext_labels):
    ax.annotate(txt, (x_values[i], y_values[i]), fontsize=10)
  plt.xlabel('Number of sources (k)', fontsize=14)
  plt.ylabel('Cumulative penalty reduction', fontsize=14)
  plt.xticks(x_values)
  ax.tick_params(axis='both', which='major', labelsize=7)
  fig.suptitle(title, fontsize=16)
  fig.savefig(plot_filepath)
  #    = create_dict_url_to_pub_country()


def runInfluenceMaximizationCelfForGeneric(in_news_websites_geo_folder, det_time_result_filepath, \
                             graph_filepath, det_time_plot_filepath, k):
  graph = nx.read_graphml(graph_filepath)
  
  print("nb connected components: ", nx.number_connected_components(graph.to_undirected()))
  print("starting celf models (detection_likelihood, detection_time, population_affected) with " + str(k) + " influential nodes ...")


  print("----------------------------")
  # # ------------------------------
  print("Goal: detection time")
  res = celf_detection_time(graph, k)
  print(res)
  solutions = res[0]
  penalty_reductions = res[1]
  mat = pd.DataFrame.from_dict({"solutions":solutions, "penalty_reductions":penalty_reductions})
  mat.to_csv(det_time_result_filepath, index=True, sep=";")
  print("----------------------------")
    
    
  
  #######################################################
  # PLOT
  #######################################################
  
  source_url_to_pub_country_code = create_dict_url_to_pub_country_code(in_news_websites_geo_folder)
  
  print("Goal: detection time")
  descr = "detection_time"
  df = pd.read_csv(det_time_result_filepath, usecols=["solutions","penalty_reductions"], sep=";")
  plot_celf_results(df, det_time_plot_filepath, descr, source_url_to_pub_country_code)
  print("ending celf model ...")
  
  
  
  
  
