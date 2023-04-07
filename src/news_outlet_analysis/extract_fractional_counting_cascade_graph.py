
import os
import numpy as np
import pandas as pd
import networkx as nx



def extractFractionalCountingCascadeGraph(event_candidates, clusters, output_dirpath, graph_filename):
  
  counter = 0
  source_to_index = {}
  sources_dict_for_pandas = {"id": [], "source": []}
  for e in event_candidates:
    if e.source not in source_to_index:
      source_to_index[e.source] = counter
      sources_dict_for_pandas["id"].append(counter)
      sources_dict_for_pandas["source"].append(e.source)
      counter = counter + 1
      
  df_source_info = pd.DataFrame.from_dict(sources_dict_for_pandas)
  source_info_filepath = os.path.join(output_dirpath,"source_id_info.txt")
  # df_source_info.to_csv(source_info_filepath, index=True, sep=";")
  
  cluster_id_to_size = []
  
  adj_matrix_counting_cascade = np.zeros((len(source_to_index.keys()), len(clusters))) # publisher vs cascade
  # print(adj_matrix_counting_cascade.shape)
  
  # cluid_to_index = dict(zip(clusters,range(len(clusters))))
  clu_id = 0
  for event_candidate_list in clusters:
    clu_id += 1
    #print("------------------")
    #print("clu_id: "+str(clu_id), [source_to_index[e.source] for e in event_candidate_list])
    cluster_id_to_size.append(len(event_candidate_list))
    #print(event_candidate_list)
    
    for e in event_candidate_list:
      source_id = source_to_index[e.source]
      adj_matrix_counting_cascade[source_id, clu_id-1] = 1
  
  #print(adj_matrix_counting_cascade)
  # np.savetxt(os.path.join(output_dirpath,"adj_matrix_sources_to_cascades.txt"),adj_matrix_counting_cascade,fmt='%d',delimiter=';')
  
  # =========================================
  # create adjacency matrix of directed publishers network
  
  adj_matrix_fractional_counting_cascade = np.zeros((len(source_to_index.keys()), len(source_to_index.keys()))) # source vs cascade
  # print(adj_matrix_fractional_counting_cascade.shape)
  
  
  for i in range(0,len(source_to_index.keys())):
    for j in range(0, len(source_to_index.keys())):
      if i<=j:
        #print(str(i)+","+str(j))
        row_i = adj_matrix_counting_cascade[i, :] / cluster_id_to_size
        row_j = adj_matrix_counting_cascade[j, :] / cluster_id_to_size
        res = np.dot(row_i,np.transpose(row_j))
        adj_matrix_fractional_counting_cascade[i,j] = res
        adj_matrix_fractional_counting_cascade[j,i] = res
      
  # np.savetxt(os.path.join(output_dirpath,"adj_matrix_undirected_sources_to_sources.txt"), adj_matrix_fractional_counting_cascade,fmt='%.2f',delimiter=';') 
  
  
  # =======================================================
  
  adj_matrix_directed_fractional_counting_cascade = np.zeros((len(source_to_index.keys()), len(source_to_index.keys()))) # source vs cascade
  # print(adj_matrix_directed_fractional_counting_cascade.shape)
  
  for i in range(0,len(source_to_index.keys())):
    diag = adj_matrix_fractional_counting_cascade[i,i]
    # print(i, diag)
    for j in range(0, len(source_to_index.keys())):
      #print(str(i)+","+str(j))
      adj_matrix_directed_fractional_counting_cascade[i,j] = adj_matrix_fractional_counting_cascade[i,j] / diag
    adj_matrix_directed_fractional_counting_cascade[i,i] = 0 # do not allow any self loop
  
  # np.savetxt(os.path.join(output_dirpath,"adj_matrix_directed_sources_to_sources.txt"), adj_matrix_directed_fractional_counting_cascade,fmt='%.2f',delimiter=';')   

  graph = nx.from_numpy_matrix(adj_matrix_directed_fractional_counting_cascade, create_using=nx.DiGraph)
  for node in graph.nodes(data=True):
    node_id = node[0]
    node[1]["name"] = sources_dict_for_pandas["source"][node_id]
  
  graph_filepath = os.path.join(output_dirpath, graph_filename)
  nx.write_graphml(graph, graph_filepath)

      
