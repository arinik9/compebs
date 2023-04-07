'''
Created on Dec 5, 2022

@author: nejat
'''


import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
from itertools import combinations 
import csv


def plot_timeliness_with_lineplot(platform1_name, platform2_name, diff_values, out_figure_filepath):
  fig = plt.figure(figsize=(10, 10))
  
  plt.plot(diff_values)
  plt.axhline(y=0, color='r', linestyle='-')
  
  plt.xlabel("Shared events in chronological order", fontsize=24)
  plt.ylabel("Time lag in days "+ platform1_name + " vs. " + platform2_name, fontsize=24)
  plt.xticks(fontsize=20)
  plt.yticks(fontsize=20)
  
  fig.savefig(out_figure_filepath)


def plot_timeliness_with_histogram(platform1_name, platform2_name, diff_values, out_figure_filepath):
  fig = plt.figure(figsize=(10, 10))
  
  n, bins, patches = plt.hist(diff_values, bins=50, density=False, facecolor='g', alpha=0.75)

  plt.xlabel('Time lag (days)', fontsize=30)
  plt.ylabel('Frequency', fontsize=30)
  plt.title(platform1_name+' vs.'+platform2_name, fontsize = 40)
  #plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
  plt.xlim(-100, 100)
  plt.ylim(0,210)
  plt.grid(True)
  plt.xticks(fontsize=20)
  plt.yticks(fontsize=20)
  
  fig.savefig(out_figure_filepath)
  
  

def compute_timeliness_for_all_platforms_old(input_folder, output_folder, platforms):

  for platform_pair in list(combinations(platforms, 2)):
    platform1_name = platform_pair[0]
    platform2_name = platform_pair[1]
    alignment_filepath = os.path.join(input_folder, platform1_name+"_"+platform2_name+"_event_matching.csv")
    df_alignment = pd.read_csv(alignment_filepath, sep=";", keep_default_na=False)

    df_alignment[platform1_name+"_date"] = pd.to_datetime(df_alignment[platform1_name+"_date"])
    df_alignment[platform2_name+"_date"] = pd.to_datetime(df_alignment[platform2_name+"_date"])

    # sort the dataframe by the the date info of the padiweb events
    df_alignment.sort_values([platform1_name+"_date"], ascending=[True], inplace=True)

    platform1_date_values = df_alignment[platform1_name+"_date"].to_list()
    platform2_date_values = df_alignment[platform2_name+"_date"].to_list()


    L = 21

    # FIRST SOURCE VS. SECOND SOURCE
    diff_values = [(platform1_date_values[i]-platform2_date_values[i]).days for i in range(len(platform1_date_values))]

    timeliness_score = 0.0
    for time_lag in diff_values:
      diff = 0.0
      if time_lag > 0.0:
        diff = time_lag
      curr_score = 1 - np.exp(-(diff/L))
      timeliness_score += curr_score
    timeliness_score = timeliness_score/len(diff_values)
    print(platform_pair, timeliness_score)

    # SECOND SOURCE VS. FIRST SOURCE
    diff_values = -np.array(diff_values)

    timeliness_score = 0.0
    for time_lag in diff_values:
      diff = 0.0
      if time_lag > 0.0:
        diff = time_lag
      curr_score = 1 - np.exp(-(diff/L))
      timeliness_score += curr_score
    timeliness_score = timeliness_score/len(diff_values)
    print(tuple(reversed(platform_pair)), timeliness_score)



def compute_timeliness_for_all_platforms(input_folder, output_folder, platforms, ref_platform):
  
  try:
    if not os.path.exists(output_folder):
      os.makedirs(output_folder)
  except OSError as err:
    print(err)
  
  for platform_name in platforms:
    alignment_filepath = os.path.join(input_folder, platform_name+"_"+ref_platform+"_event_matching.csv")
    df_alignment = pd.read_csv(alignment_filepath, sep=";", keep_default_na=False)

    df_alignment[platform_name+"_date"] = pd.to_datetime(df_alignment[platform_name+"_date"])
    df_alignment[ref_platform+"_date"] = pd.to_datetime(df_alignment[ref_platform+"_date"])
    
    # sort the dataframe by the the date info of the padiweb events
    df_alignment.sort_values([platform_name+"_date"], ascending=[True], inplace=True)

    platform1_date_values = df_alignment[platform_name+"_date"].to_list()
    platform2_date_values = df_alignment[ref_platform+"_date"].to_list()
    
    
    L = 21
    
    # FIRST SOURCE VS. SECOND SOURCE
    diff_values = [(platform1_date_values[i]-platform2_date_values[i]).days for i in range(len(platform1_date_values))]

    timeliness_score = 0.0
    for time_lag in diff_values:
      diff = 0.0
      if time_lag > 0.0:
        diff = time_lag
      curr_score = 1 - np.exp(-(diff/L))
      timeliness_score += curr_score
    timeliness_score = timeliness_score/len(diff_values)
    print(platform_name, "vs", ref_platform, timeliness_score)
    
    df = pd.DataFrame.from_dict({"timeliness": [timeliness_score]})
    res_eval_filepath = os.path.join(output_folder, "timeliness_"+platform_name+".csv")
    df.to_csv(res_eval_filepath, sep=";", quoting=csv.QUOTE_NONNUMERIC)



def plot_timeliness_for_all_platforms_old(input_folder, output_folder, platforms):
  
  try:
    if not os.path.exists(output_folder):
      os.makedirs(output_folder)
  except OSError as err:
     print(err)
  
  
  for platform_pair in list(combinations(platforms, 2)):
    platform1_name = platform_pair[0]
    platform2_name = platform_pair[1]
    alignment_filepath = os.path.join(input_folder, platform1_name+"_"+platform2_name+"_event_matching.csv")
    df_alignment = pd.read_csv(alignment_filepath, sep=";", keep_default_na=False)

    df_alignment[platform1_name+"_date"] = pd.to_datetime(df_alignment[platform1_name+"_date"])
    df_alignment[platform2_name+"_date"] = pd.to_datetime(df_alignment[platform2_name+"_date"])
    
    # sort the dataframe by the the date info of the padiweb events
    df_alignment.sort_values([platform1_name+"_date"], ascending=[True], inplace=True)

    platform1_date_values = df_alignment[platform1_name+"_date"].to_list()
    platform2_date_values = df_alignment[platform2_name+"_date"].to_list()
    
    diff_values = [(platform1_date_values[i]-platform2_date_values[i]).days for i in range(len(platform1_date_values))]

    np_diff_values = np.array(diff_values)
    np_diff_values1 = np_diff_values[np_diff_values>0]
    #print(platform_pair, np.mean(np_diff_values1))
    np_diff_values2 = -np_diff_values[np_diff_values<0]
    #print(tuple(reversed(platform_pair)), np.mean(np_diff_values2))
    #print(platform_pair, len(np_diff_values))
    #print(platform_pair, len(np_diff_values[np_diff_values>0]), len(np_diff_values[np_diff_values<0]))
    #print(platform_pair, len(np_diff_values[np_diff_values>30]), len(np_diff_values[np_diff_values<-30]))
    
    out_figure_filepath = os.path.join(output_folder, "timeliness-lineplot_" + platform1_name+"_"+platform2_name+".png")
    plot_timeliness_with_lineplot(platform1_name, platform2_name, diff_values, out_figure_filepath)

    out_figure_filepath = os.path.join(output_folder, "timeliness-histogram_" + platform1_name+"_"+platform2_name+".png")
    plot_timeliness_with_histogram(platform1_name, platform2_name, diff_values, out_figure_filepath)



def plot_timeliness_for_all_platforms(input_folder, output_folder, platforms, ref_platform):
  
  try:
    if not os.path.exists(output_folder):
      os.makedirs(output_folder)
  except OSError as err:
     print(err)
  
  
  for platform_name in platforms:
    alignment_filepath = os.path.join(input_folder, platform_name+"_"+ref_platform+"_event_matching.csv")
    df_alignment = pd.read_csv(alignment_filepath, sep=";", keep_default_na=False)

    df_alignment[platform_name+"_date"] = pd.to_datetime(df_alignment[platform_name+"_date"])
    df_alignment[ref_platform+"_date"] = pd.to_datetime(df_alignment[ref_platform+"_date"])
    
    # sort the dataframe by the the date info of the padiweb events
    df_alignment.sort_values([platform_name+"_date"], ascending=[True], inplace=True)

    platform1_date_values = df_alignment[platform_name+"_date"].to_list()
    platform2_date_values = df_alignment[ref_platform+"_date"].to_list()
    
    diff_values = [(platform1_date_values[i]-platform2_date_values[i]).days for i in range(len(platform1_date_values))]

    np_diff_values = np.array(diff_values)
    np_diff_values1 = np_diff_values[np_diff_values>0]
    #print(platform_pair, np.mean(np_diff_values1))
    np_diff_values2 = -np_diff_values[np_diff_values<0]
    #print(tuple(reversed(platform_pair)), np.mean(np_diff_values2))
    #print(platform_pair, len(np_diff_values))
    #print(platform_pair, len(np_diff_values[np_diff_values>0]), len(np_diff_values[np_diff_values<0]))
    #print(platform_pair, len(np_diff_values[np_diff_values>30]), len(np_diff_values[np_diff_values<-30]))
    
    out_figure_filepath = os.path.join(output_folder, "timeliness-lineplot_" + platform_name+"_"+ref_platform+".png")
    plot_timeliness_with_lineplot(platform_name, ref_platform, diff_values, out_figure_filepath)

    out_figure_filepath = os.path.join(output_folder, "timeliness-histogram_" + platform_name+"_"+ref_platform+".png")
    plot_timeliness_with_histogram(platform_name, ref_platform, diff_values, out_figure_filepath)  

  