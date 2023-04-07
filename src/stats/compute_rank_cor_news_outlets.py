'''
Created on Nov 30, 2022

@author: nejat
'''

import numpy as np


def compute_Kishida_normalized_recall(df_ranking_ref, df_ranking_cand, nb_limit=1000):
  if df_ranking_ref.shape[0]>nb_limit:
    df_ranking_ref = df_ranking_ref.iloc[0:nb_limit]
  if df_ranking_cand.shape[0]>nb_limit:
    df_ranking_cand = df_ranking_cand.iloc[0:nb_limit]
    
  df_ranking_ref.index = df_ranking_ref['solutions']
  df_ranking_cand.index = df_ranking_cand['solutions']
  
  df_ranking_ref['rank'] = range(df_ranking_ref.shape[0])
  df_ranking_cand['rank'] = range(df_ranking_cand.shape[0])
  
  l1 = list(df_ranking_ref['solutions'].to_numpy())#[0:REF_LIMIT])
  l2 = df_ranking_cand['solutions'].to_list()
  common_news_outlets = list(set(l1).intersection(l2))
  
  R = len(common_news_outlets)
  N = df_ranking_ref.shape[0]
  
  ideal_list = df_ranking_ref.loc[common_news_outlets,"solutions"].to_numpy()
  
  df_ranking_cand["relevant"] = 0 # init
  df_ranking_cand.loc[common_news_outlets,"relevant"] = 1
  
  diff_sum = 0
  for i in range(R):
    news_outlet = ideal_list[i]
    ri = df_ranking_ref.loc[news_outlet, "rank"]
    diff_sum += (ri - i)
    
  norm_recall = 0
  if R>0:
    norm_value = 0
    if N != R:
      denom = (R*N - R*R)
      norm_value = diff_sum/denom
    norm_recall = 1 - norm_value
  return norm_recall, R


def compute_Kishida_normalized_precision(df_ranking_ref, df_ranking_cand, nb_limit=1000):
  if df_ranking_ref.shape[0]>nb_limit:
    df_ranking_ref = df_ranking_ref.iloc[0:nb_limit]
  if df_ranking_cand.shape[0]>nb_limit:
    df_ranking_cand = df_ranking_cand.iloc[0:nb_limit]
      
  df_ranking_ref.index = df_ranking_ref['solutions']
  df_ranking_cand.index = df_ranking_cand['solutions']
  
  df_ranking_ref['rank'] = range(df_ranking_ref.shape[0])
  df_ranking_cand['rank'] = range(df_ranking_cand.shape[0])
  
  l1 = list(df_ranking_ref['solutions'].to_numpy())
  l2 = df_ranking_cand['solutions'].to_list()
  common_news_outlets = list(set(l1).intersection(l2))
  
  R = len(common_news_outlets)
  N = df_ranking_ref.shape[0]
  
  ideal_list = df_ranking_ref.loc[common_news_outlets,"solutions"].to_numpy()
  
  df_ranking_cand["relevant"] = 0 # init
  df_ranking_cand.loc[common_news_outlets,"relevant"] = 1
 
  
  diff_sum = 0
  denom = 0.0
  for i in range(R):
    pattern = ideal_list[i]
    ri = df_ranking_ref.loc[pattern, "rank"]
    diff_sum += (np.log(ri+1) - np.log(i+1)) # we put +1 to avoid log(0)
    
  norm_precision = 0
  if R>0:
    norm_value = 0
    if N != R:
      denom = np.log(np.math.factorial(N)/(np.math.factorial(R) * np.math.factorial(N-R)))
      norm_value = diff_sum/denom
    norm_precision = 1 - norm_value
  return norm_precision, R



def compute_Kishida_normalized_fmeasure(df_ranking_ref, df_ranking_cand, nb_limit=1000):
  recall_val, nb_common_patterns = compute_Kishida_normalized_recall(df_ranking_ref, df_ranking_cand, nb_limit)
  precision_val, nb_common_patterns = compute_Kishida_normalized_precision(df_ranking_ref, df_ranking_cand, nb_limit)
  fmeasure_val = 0.0
  if recall_val>0 and precision_val>0:
    fmeasure_val = 2*(recall_val*precision_val)/(recall_val+precision_val)
  # 
  return fmeasure_val
          


  