'''
Created on Nov 18, 2022

@author: nejat
'''

import numpy as np
import networkx as nx

from util_event import read_events_from_df




def create_heterogeneous_graph_from_events(in_taxonomy_folder, df_events, out_graph_filepath, geonameId_to_name, \
                                            geonameId_to_lat, geonameId_to_lng, geonameId_to_hier_level):
  events = read_events_from_df(df_events, in_taxonomy_folder)
  
  graph = nx.DiGraph()
  
  for e in events:
    
    # -------------------------------------------------------
    # prepare event date for graph
    # -------------------------------------------------------
    
    loc = e.loc
    # output: [123, 124, 125]
    disease_info_list = e.disease.get_entry()
    # intermediate output: ["", "AI"]
    disease_info_list = [d for d in disease_info_list if d != ""]
    # output: ["AI"]
    host_info_list_of_tuples = e.host.get_unnested_entry()
    print("--", host_info_list_of_tuples)
    # host_info_tuple[0]: level 1 -> single value
    # host_info_tuple[1]: level 2 -> a list of values
    # intermediate output: [('b', [1, 2, 5]), ('c', [4, 6, 7]), ('d', [11, 12, 13]), ('e', [66])]
    host_info_list = []
    for host_info_tuple in host_info_list_of_tuples:
      added = False
      for val in host_info_tuple[1]:
        if "unknown" not in val:
          host_info_list.append((host_info_tuple[0], val))
          added = True
      if not added and "unknown": #not in host_info_tuple[0]:
        host_info_list.append((host_info_tuple[0],))
    # output: [('a', 'b', 1), ('a', 'b', 2), ('a', 'b', 5), ('a', 'c', 4), ('a', 'c', 6), ('a', 'c', 7), ('r', 'd', 11), ('r', 'd', 12), ('r', 'd', 13), ('r', 'e', 66)
    
    
    # -------------------------------------------------------
    # add nodes
    # -------------------------------------------------------
    
    # add event node
    if not graph.has_node(e.e_id):
      graph.add_node(e.e_id, type="event", date=str(e.date.get_entry()))
        
    # add loc nodes
    for l_id in loc.hierarchy_data:
      if not graph.has_node(l_id):
        name = geonameId_to_name[l_id]
        lat = geonameId_to_lat[l_id]
        lng = geonameId_to_lng[l_id]
        hier_level = geonameId_to_hier_level[l_id]
        graph.add_node(l_id, type="location", name=name, lat=lat, lng=lng, hier_level=hier_level)
        
    # add disease nodes
    for d in disease_info_list:
      if not graph.has_node(d):
        graph.add_node(d, type="disease")
        
    # add host nodes
    for host_info in host_info_list:
      for h in host_info:
        if not graph.has_node(h):
          graph.add_node(h, type="host")
          
    # -------------------------------------------------------
    # add hierarchical (inner-attribute) links
    # -------------------------------------------------------
            
    # add links among loc nodes
      # in loc.hierarchy_data the hierarchy order: from most generalized level to more specific level
    if len(loc.hierarchy_data)>1:
      for i in range(len(loc.hierarchy_data)-1):
        prev_l_id = loc.hierarchy_data[i]
        curr_l_id = loc.hierarchy_data[i+1]
        # from genaral level to specific level
        if graph.has_edge(prev_l_id, curr_l_id):
          graph[prev_l_id][curr_l_id]["weight"] += 1
        else:
          graph.add_edge(prev_l_id, curr_l_id, weight=1, type="down_hierarchy")
        # from specific level to genaral level
        if graph.has_edge(curr_l_id, prev_l_id):
          graph[curr_l_id][prev_l_id]["weight"] += 1
        else:
          graph.add_edge(curr_l_id, prev_l_id, weight=1, type="up_hierarchy")  

    # add links among disease nodes
      # in disease_info_list the hierarchy order: from most specific level to more generalized level
    if len(disease_info_list)>1:
      for i in range(len(disease_info_list)-1):
        prev_d = disease_info_list[i]
        curr_d = disease_info_list[i+1]
        if prev_d != "" and curr_d != "":
          # from specific level to genaral level
          if graph.has_edge(prev_d, curr_d):
            graph[prev_d][curr_d]["weight"] += 1
          else:
            graph.add_edge(prev_d, curr_d, weight=1, type="up_hierarchy")
          # from genaral level to specific level
          if graph.has_edge(curr_d, prev_d):
            graph[curr_d][prev_d]["weight"] += 1
          else:
            graph.add_edge(curr_d, prev_d, weight=1, type="down_hierarchy")
        
          
    # add links among host nodes
      # in host_info_list the hierarchy order: from most generalized level to more specific level
    for host_info in host_info_list:
      if len(host_info)>1:
        for i in range(len(host_info)-1):
          prev_h = host_info[i]
          curr_h = host_info[i+1]
          # from genaral level to specific level
          if graph.has_edge(prev_h, curr_h):
            graph[prev_h][curr_h]["weight"] += 1
          else:
            graph.add_edge(prev_h, curr_h, weight=1, type="down_hierarchy")
          # from specific level to genaral level
          if graph.has_edge(curr_h, prev_h):
            graph[curr_h][prev_h]["weight"] += 1
          else:
            graph.add_edge(curr_h, prev_h, weight=1, type="up_hierarchy")
          
    # -------------------------------------------------------
    # add event-attribute links
    # -------------------------------------------------------  
    
    host_last_hier_values = list(np.unique([host_info[-1] for host_info in host_info_list]))
    data_for_links = [loc.hierarchy_data[-1], disease_info_list[0]] + host_last_hier_values
    
    for t in data_for_links:
      if graph.has_edge(e.e_id, t):
        graph[e.e_id][t]["weight"] += 1
      else:
        graph.add_edge(e.e_id, t, weight=1, type="attribute")  
    
  # -------------------------------------------------------
  # write the graph into file
  # -------------------------------------------------------
  
  print("nb nodes:" + str(graph.number_of_nodes()) + " and nb edges:" + str(graph.number_of_edges()))
  nx.write_graphml(graph, out_graph_filepath)
  print("finished to write the graph into this path: " + out_graph_filepath)
  
  # # -------------------------------------------------------
  # # write the graph into file
  # # -------------------------------------------------------
  #
  # # Data File Format 
  # # "t # N" means the Nth graph,
  # # "v M L" means that the Mth vertex in this graph has label L,
  # # "e P Q L" means that there is an edge connecting the Pth vertex with the Qth vertex. The edge has label L.
  # # example: https://github.com/NaazS03/cgSpan/blob/master/graphdata/graph.data.1
  # node2index = dict(zip(list(graph.nodes), range(graph.number_of_nodes())))
  # file_lines = ["t # 0"]
  # for v in list(graph.nodes):
  #   line_content = "v " + str(node2index[v]) + " " + str(v)
  #   file_lines.append(line_content)
  # for e in list(graph.edges(data=True)):
  #   s = e[0]
  #   t = e[1]
  #   w = e[2]["weight"]
  #   line_content = "e " + str(node2index[s]) + " " + str(node2index[t]) + " " + str(w)
  #   file_lines.append(line_content)
  # file_lines.append("t # -1")
  # file_content = "\n".join(file_lines)
  # graph_filepath = os.path.join(out_graph_folder, "event_cooccurence.txt")
  # with open(graph_filepath, 'w') as f:
  #   f.write(file_content)
      
      


# if __name__ == '__main__':
#
#   events_filepath = os.path.join(consts.IN_PADIWEB_FOLDER, "events.csv") 
#   out_graph_folder = consts.OUT_GRAPH_PADIWEB_FOLDER
#
#   try:
#     if not os.path.exists(consts.OUT_GRAPH_PADIWEB_FOLDER):
#       os.makedirs(consts.OUT_GRAPH_PADIWEB_FOLDER)
#   except OSError as err:
#     print(err)
#
#   out_preprocessing_folder = consts.OUT_PREPROCESSING_PADIWEB_FOLDER
#   result_filepath = os.path.join(out_preprocessing_folder, "geonames_info.csv")
#   df = pd.read_csv(result_filepath, sep=";", keep_default_na=False)
#   geonameId_to_name = dict(zip(df["geonames_id"], df["name"]))
#   geonameId_to_lat = dict(zip(df["geonames_id"], df["lat"]))
#   geonameId_to_lng = dict(zip(df["geonames_id"], df["lng"]))
#   geonameId_to_hier_level = dict(zip(df["geonames_id"], df["hier_level"].apply(lambda x: len(x))))
#
#   df_events = read_df_events(events_filepath)
#   out_graph_filepath = os.path.join(out_graph_folder, "event_hin.graphml")
#   create_heterogeneous_graph_from_events(df_events, out_graph_filepath, geonameId_to_name, \
#                                           geonameId_to_lat, geonameId_to_lng, geonameId_to_hier_level)
  
  