

import networkx as nx



# https://github.com/zahraDehghanian97/CELF
# https://github.com/mohsentaherinia/OptimizedCELF






# create a chain graph
def add_nodes_and_links_from_event_candidate_list(graph, event_candidate_list, cluster_id):
    
  newlist = sorted(event_candidate_list, key=lambda e: e.date.get_entry(), reverse=False)
  #if cluster_id == 2:
  #  print(newlist)
  for e in newlist:
    #print(e.e_id)
    if not graph.has_node(e.e_id):
      graph.add_node(e.e_id, source=e.source, cluster=cluster_id, country_mention=e.loc.country_code, date=str(e.date.get_entry()), article_id=e.article_id)

  for i in range(1,len(newlist)):
    source = newlist[i].e_id
    target = newlist[i-1].e_id
    time_diff = (newlist[i].date.get_entry() - newlist[i-1].date.get_entry()).days
    if graph.has_edge(source, target):
      if time_diff < graph[source][target]["weight"]:
        graph[source][target]["weight"] = time_diff
    else:
      graph.add_edge(source, target, weight=time_diff)    
  return(graph)



def extractLeskovecCascadeGraphForGeneric(event_canditates, clusters, graph_filepath):
  
  graph = nx.DiGraph()
  clu_id = 0
  for event_candidate_list in clusters:
    clu_id += 1
    print("------------------")
    print("clu_id: "+str(clu_id))
    # if clu_id == 2:
    #   print(event_candidate_list)
    # if len(event_candidate_list)>1:
    graph = add_nodes_and_links_from_event_candidate_list(graph, event_candidate_list, clu_id)
    # else:
    #   print(event_candidate_list[0].source)
  # print("nb connected components: ", nx.number_connected_components(graph.to_undirected()))
  nx.write_graphml(graph, graph_filepath)
  


  

# def extractLeskovecCascadeGraphForPadiweb(single_event_classif_strategy, event_retrieval_strategy, event_clustering:AbstractEventClustering):
#
#   input_dirpath = consts.CSV_PADIWEB_FOLDER
#   output_dirpath = consts.INFLUENCE_MAX_PADIWEB_FOLDER
#
#   # signal_filepath = os.path.join(consts.IN_PADIWEB_FOLDER, \
#   #                         consts.PADIWEB_SIGNAL_CSV_FILENAME + "." + consts.FILE_FORMAT_CSV)
#   # signal_info_exists = os.path.isfile(signal_filepath)
#
#   choice_strategy_descr_prev = "task1=" + single_event_classif_strategy.get_description() \
#                         + "_task2=" + event_retrieval_strategy.get_description()
#   choice_strategy_descr = choice_strategy_descr_prev + "_task3=" + event_clustering.get_description()
#   event_candidates_filepath = os.path.join(input_dirpath, \
#                               consts.PADIWEB_EVENT_CANDIDATES + "_by time_interval" \
#                                + "_" + choice_strategy_descr + "." + consts.FILE_FORMAT_CSV)
#
#   df_event_candidates = read_df_event_candidates(event_candidates_filepath)
#   graph_filepath = os.path.join(output_dirpath,"leskovec_cascade_graph_"+choice_strategy_descr+".graphml")
#
#   extractLeskovecCascadeGraphForGeneric(df_event_candidates, output_dirpath, graph_filepath)
#
#
#
#
#
# def extractAsiaLeskovecCascadeGraphForPadiweb(single_event_classif_strategy, event_retrieval_strategy, event_clustering:AbstractEventClustering):
#
#   input_dirpath = consts.CSV_PADIWEB_FOLDER
#   output_dirpath = consts.INFLUENCE_MAX_ASIA_PADIWEB_FOLDER
#
#   # signal_filepath = os.path.join(consts.IN_PADIWEB_FOLDER, \
#   #                         consts.PADIWEB_SIGNAL_CSV_FILENAME + "." + consts.FILE_FORMAT_CSV)
#   # signal_info_exists = os.path.isfile(signal_filepath)
#
#   choice_strategy_descr_prev = "task1=" + single_event_classif_strategy.get_description() \
#                         + "_task2=" + event_retrieval_strategy.get_description()
#   choice_strategy_descr = choice_strategy_descr_prev + "_task3=" + event_clustering.get_description()
#   asia_event_candidates_filepath = os.path.join(input_dirpath, \
#                               consts.PADIWEB_EVENT_CANDIDATES + "_asia_by time_interval" \
#                                + "_" + choice_strategy_descr + "." + consts.FILE_FORMAT_CSV)
#
#   if not os.path.exists(asia_event_candidates_filepath):
#     event_candidates_filepath = os.path.join(input_dirpath, \
#                           consts.PADIWEB_EVENT_CANDIDATES + "_by time_interval" \
#                            + "_" + choice_strategy_descr + ".csv")
#     df_event_candidates = read_df_event_candidates(event_candidates_filepath)
#     df_event_candidates = retrieve_asia_df_event_candidates(df_event_candidates)
#     df_event_candidates.to_csv(asia_event_candidates_filepath, sep=";")
#   else:
#     df_event_candidates = read_df_event_candidates(asia_event_candidates_filepath)
#
#   graph_filepath = os.path.join(output_dirpath,"asia_leskovec_cascade_graph_"+choice_strategy_descr+".graphml")
#
#   extractLeskovecCascadeGraphForGeneric(df_event_candidates, output_dirpath, graph_filepath)
#
#
#
#
#
# def extractNorthAmericaLeskovecCascadeGraphForPadiweb(single_event_classif_strategy, event_retrieval_strategy, event_clustering:AbstractEventClustering):
#   input_dirpath = consts.CSV_PADIWEB_FOLDER
#   output_dirpath = consts.INFLUENCE_MAX_NORTH_AMERICA_PADIWEB_FOLDER
#
#   # signal_filepath = os.path.join(consts.IN_PADIWEB_FOLDER, \
#   #                         consts.PADIWEB_SIGNAL_CSV_FILENAME + "." + consts.FILE_FORMAT_CSV)
#   # signal_info_exists = os.path.isfile(signal_filepath)
#
#   choice_strategy_descr_prev = "task1=" + single_event_classif_strategy.get_description() \
#                         + "_task2=" + event_retrieval_strategy.get_description()
#   choice_strategy_descr = choice_strategy_descr_prev + "_task3=" + event_clustering.get_description()
#   asia_event_candidates_filepath = os.path.join(input_dirpath, \
#                               consts.PADIWEB_EVENT_CANDIDATES + "_north_america_by time_interval" \
#                                + "_" + choice_strategy_descr + "." + consts.FILE_FORMAT_CSV)
#
#   if not os.path.exists(asia_event_candidates_filepath):
#     event_candidates_filepath = os.path.join(input_dirpath, \
#                           consts.PADIWEB_EVENT_CANDIDATES + "_by time_interval" \
#                            + "_" + choice_strategy_descr + ".csv")
#     df_event_candidates = read_df_event_candidates(event_candidates_filepath)
#     df_event_candidates = retrieve_asia_df_event_candidates(df_event_candidates)
#     df_event_candidates.to_csv(asia_event_candidates_filepath, sep=";")
#   else:
#     df_event_candidates = read_df_event_candidates(asia_event_candidates_filepath)
#
#   graph_filepath = os.path.join(output_dirpath,"north_america_leskovec_cascade_graph_"+choice_strategy_descr+".graphml")
#
#   extractLeskovecCascadeGraphForGeneric(df_event_candidates, output_dirpath, graph_filepath)
#
#
#
#
# def extractEuropeLeskovecCascadeGraphForPadiweb(single_event_classif_strategy, event_retrieval_strategy, event_clustering:AbstractEventClustering):
#
#   input_dirpath = consts.CSV_PADIWEB_FOLDER
#   output_dirpath = consts.INFLUENCE_MAX_EUROPE_PADIWEB_FOLDER
#
#   # signal_filepath = os.path.join(consts.IN_PADIWEB_FOLDER, \
#   #                         consts.PADIWEB_SIGNAL_CSV_FILENAME + "." + consts.FILE_FORMAT_CSV)
#   # signal_info_exists = os.path.isfile(signal_filepath)
#
#   choice_strategy_descr_prev = "task1=" + single_event_classif_strategy.get_description() \
#                         + "_task2=" + event_retrieval_strategy.get_description()
#   choice_strategy_descr = choice_strategy_descr_prev + "_task3=" + event_clustering.get_description()
#   asia_event_candidates_filepath = os.path.join(input_dirpath, \
#                               consts.PADIWEB_EVENT_CANDIDATES + "_europe_by time_interval" \
#                                + "_" + choice_strategy_descr + "." + consts.FILE_FORMAT_CSV)
#
#   if not os.path.exists(asia_event_candidates_filepath):
#     event_candidates_filepath = os.path.join(input_dirpath, \
#                           consts.PADIWEB_EVENT_CANDIDATES + "_by time_interval" \
#                            + "_" + choice_strategy_descr + ".csv")
#     df_event_candidates = read_df_event_candidates(event_candidates_filepath)
#     df_event_candidates = retrieve_asia_df_event_candidates(df_event_candidates)
#     df_event_candidates.to_csv(asia_event_candidates_filepath, sep=";")
#   else:
#     df_event_candidates = read_df_event_candidates(asia_event_candidates_filepath)
#
#   graph_filepath = os.path.join(output_dirpath,"europe_leskovec_cascade_graph_"+choice_strategy_descr+".graphml")
#
#   extractLeskovecCascadeGraphForGeneric(df_event_candidates, output_dirpath, graph_filepath)
#
#
#
#
#
# def extractLeskovecCascadeGraphForHealthmap(event_clustering:AbstractEventClustering):
#
#   input_dirpath = consts.CSV_HEALTHMAP_FOLDER
#   output_dirpath = consts.INFLUENCE_MAX_HEALTHMAP_FOLDER
#
#   # signal_filepath = os.path.join(consts.IN_PADIWEB_FOLDER, \
#   #                         consts.PADIWEB_SIGNAL_CSV_FILENAME + "." + consts.FILE_FORMAT_CSV)
#   # signal_info_exists = os.path.isfile(signal_filepath)
#
#   choice_strategy_descr = "task3=" + event_clustering.get_description()
#   event_candidates_filepath = os.path.join(input_dirpath, \
#                               consts.HEALTHMAP_EVENT_CANDIDATES + "_by time_interval" \
#                                + "_" + choice_strategy_descr + "." + consts.FILE_FORMAT_CSV)
#
#   df_event_candidates = read_df_event_candidates(event_candidates_filepath)
#   graph_filepath = os.path.join(output_dirpath,"leskovec_cascade_graph_"+choice_strategy_descr+".graphml")
#
#   extractLeskovecCascadeGraphForGeneric(df_event_candidates, output_dirpath, graph_filepath)
#
#
#
#
# def extractAsiaLeskovecCascadeGraphForHealthmap(event_clustering:AbstractEventClustering):
#
#   input_dirpath = consts.CSV_HEALTHMAP_FOLDER
#   output_dirpath = consts.INFLUENCE_MAX_ASIA_HEALTHMAP_FOLDER
#
#   # signal_filepath = os.path.join(consts.IN_PADIWEB_FOLDER, \
#   #                         consts.PADIWEB_SIGNAL_CSV_FILENAME + "." + consts.FILE_FORMAT_CSV)
#   # signal_info_exists = os.path.isfile(signal_filepath)
#
#   choice_strategy_descr = "task3=" + event_clustering.get_description()
#   asia_event_candidates_filepath = os.path.join(input_dirpath, \
#                               consts.HEALTHMAP_EVENT_CANDIDATES + "_asia_by time_interval" \
#                                + "_" + choice_strategy_descr + "." + consts.FILE_FORMAT_CSV)
#
#   if not os.path.exists(asia_event_candidates_filepath):
#     event_candidates_filepath = os.path.join(input_dirpath, \
#                           consts.HEALTHMAP_EVENT_CANDIDATES + "_by time_interval" \
#                            + "_" + choice_strategy_descr + ".csv")
#     df_event_candidates = read_df_event_candidates(event_candidates_filepath)
#     df_event_candidates = retrieve_asia_df_event_candidates(df_event_candidates)
#     df_event_candidates.to_csv(asia_event_candidates_filepath, sep=";")
#   else:
#     df_event_candidates = read_df_event_candidates(asia_event_candidates_filepath)
#
#   graph_filepath = os.path.join(output_dirpath,"asia_leskovec_cascade_graph_"+choice_strategy_descr+".graphml")
#
#   extractLeskovecCascadeGraphForGeneric(df_event_candidates, output_dirpath, graph_filepath)
#
#
#
# def extractNorthAmericaLeskovecCascadeGraphForHealthmap(event_clustering:AbstractEventClustering):
#
#   input_dirpath = consts.CSV_HEALTHMAP_FOLDER
#   output_dirpath = consts.INFLUENCE_MAX_NORTH_AMERICA_HEALTHMAP_FOLDER
#
#
#   # signal_filepath = os.path.join(consts.IN_PADIWEB_FOLDER, \
#   #                         consts.PADIWEB_SIGNAL_CSV_FILENAME + "." + consts.FILE_FORMAT_CSV)
#   # signal_info_exists = os.path.isfile(signal_filepath)
#
#   choice_strategy_descr = "task3=" + event_clustering.get_description()
#   asia_event_candidates_filepath = os.path.join(input_dirpath, \
#                               consts.HEALTHMAP_EVENT_CANDIDATES + "_north_america_by time_interval" \
#                                + "_" + choice_strategy_descr + "." + consts.FILE_FORMAT_CSV)
#
#   if not os.path.exists(asia_event_candidates_filepath):
#     event_candidates_filepath = os.path.join(input_dirpath, \
#                           consts.HEALTHMAP_EVENT_CANDIDATES + "_by time_interval" \
#                            + "_" + choice_strategy_descr + ".csv")
#     df_event_candidates = read_df_event_candidates(event_candidates_filepath)
#     df_event_candidates = retrieve_asia_df_event_candidates(df_event_candidates)
#     df_event_candidates.to_csv(asia_event_candidates_filepath, sep=";")
#   else:
#     df_event_candidates = read_df_event_candidates(asia_event_candidates_filepath)
#
#   graph_filepath = os.path.join(output_dirpath,"north_america_leskovec_cascade_graph_"+choice_strategy_descr+".graphml")
#
#   extractLeskovecCascadeGraphForGeneric(df_event_candidates, output_dirpath, graph_filepath)
#
#
#
#
# def extractEuropeLeskovecCascadeGraphForHealthmap(event_clustering:AbstractEventClustering):
#
#   input_dirpath = consts.CSV_HEALTHMAP_FOLDER
#   output_dirpath = consts.INFLUENCE_MAX_EUROPE_HEALTHMAP_FOLDER
#
#   # signal_filepath = os.path.join(consts.IN_PADIWEB_FOLDER, \
#   #                         consts.PADIWEB_SIGNAL_CSV_FILENAME + "." + consts.FILE_FORMAT_CSV)
#   # signal_info_exists = os.path.isfile(signal_filepath)
#
#   choice_strategy_descr = "task3=" + event_clustering.get_description()
#   asia_event_candidates_filepath = os.path.join(input_dirpath, \
#                               consts.HEALTHMAP_EVENT_CANDIDATES + "_europe_by time_interval" \
#                                + "_" + choice_strategy_descr + "." + consts.FILE_FORMAT_CSV)
#
#   if not os.path.exists(asia_event_candidates_filepath):
#     event_candidates_filepath = os.path.join(input_dirpath, \
#                           consts.HEALTHMAP_EVENT_CANDIDATES + "_by time_interval" \
#                            + "_" + choice_strategy_descr + ".csv")
#     df_event_candidates = read_df_event_candidates(event_candidates_filepath)
#     df_event_candidates = retrieve_asia_df_event_candidates(df_event_candidates)
#     df_event_candidates.to_csv(asia_event_candidates_filepath, sep=";")
#   else:
#     df_event_candidates = read_df_event_candidates(asia_event_candidates_filepath)
#
#   graph_filepath = os.path.join(output_dirpath,"europe_leskovec_cascade_graph_"+choice_strategy_descr+".graphml")
#
#   extractLeskovecCascadeGraphForGeneric(df_event_candidates, output_dirpath, graph_filepath)
#

  
    