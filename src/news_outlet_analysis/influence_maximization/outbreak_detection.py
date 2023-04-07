'''
Created on Dec 9, 2021

@author: nejat
'''

import networkx as nx
import numpy as np
import heapq # for CLEF
import time
import queue

from event.temporality import Temporality


T_MAX = 14 # days >> 2 weeks >> constant term for penalty_reduction_detection_time
#T_MAX = 21 # days >> 2 weeks >> constant term for penalty_reduction_detection_time



def create_cascades_dict(graph):
  countries = []
  for node, attr_dict in graph.nodes(data=True):
    if attr_dict["country_mention"] not in countries:
      countries.append(attr_dict["country_mention"])
      
  cascades_dict = {}
  for node, attr_dict in graph.nodes(data=True):
    cluster = attr_dict["cluster"]
    if cluster != -1:
      if cluster not in cascades_dict:
        cascades_dict[cluster] = []
      if node not in cascades_dict[cluster]:
        cascades_dict[cluster].append(node)
  
  ids = list(cascades_dict.keys())
  sizes = [len(v) for v in cascades_dict.values()]
  cascades_dict["nb_distinct_sources"] = list(map(lambda x: len(list(set([graph.nodes[v]["source"] for v in x]))), list(cascades_dict.values())))
  cascades_dict["id"] = ids
  cascades_dict["size"] = sizes
  cascades_dict["proba"] = [1/len(cascades_dict["id"])]*len(cascades_dict["id"]) # uniform dist
  cascades_dict["nb_distinct_mention_countries"]= len(countries)
  # cascades_dict["proba"] = final_dict["size"]/sum(final_dict["size"]) # weighted dist
  return(cascades_dict)


def divide_into_cascade_subgraphs(graph, cascades_dict):
  subgraphs = []
  
  for cascade_i in cascades_dict["id"]:
    subgraph = graph.subgraph(cascades_dict[cascade_i])
    subgraphs.append(subgraph)
  return(subgraphs)



# def identify_cascade_starting_node(graph):
#   # each node object is a tuple with 2 elements: 1st element: node id, 2nd element: node attrs
#   sorted_nodes = sorted(graph.nodes(data=True), key=lambda x: Temporality(x[1]["date"]).date, reverse=False)
#   return(sorted_nodes[0][0])
#
#
# # ----------------------------------------------------------------------
#
#
# def create_dict_outbreak_detection_binary(graph, cascades_dict):
#   cascade_ids = cascades_dict["id"] 
#
#   # init
#   dict_outbreak_detection_binary = {}
#   for node, attr_dict in graph.nodes(data=True):
#     source = attr_dict["source"]
#     for cascade_i in cascade_ids:
#       if source not in dict_outbreak_detection_binary:
#         dict_outbreak_detection_binary[source] = {}
#       dict_outbreak_detection_binary[source][cascade_i] = 0 # not involved in an outbreak
#
#   S = divide_into_cascade_subgraphs(graph, cascades_dict)
#
#   for subgraph in S:
#     # get the cascade id from the first node
#     cascade_i = -1
#     for node, attr_dict in subgraph.nodes(data=True):
#       cascade_i = attr_dict["cluster"]
#       break
#
#     cascade_starting_node = identify_cascade_starting_node(subgraph)
#
#     # iterate over the nodes of the subgraph
#     for node, attr_dict in subgraph.nodes(data=True):
#       source = attr_dict["source"]
#       dict_outbreak_detection_binary[source][cascade_i] = int(nx.has_path(subgraph, node, cascade_starting_node)) # involved in an outbreak
#   return(dict_outbreak_detection_binary)
#
#
# # 0: outbreak not detected
# # 1: outbreak detected
# # def lookup_outbreak_detection_bool(dict_outbreak_detection_binary, source, cascade):
# #   return(dict_outbreak_detection_binary[source][cascade])
#
#
# def penalty_reduction_detection_likelihood(dict_outbreak_detection_binary, sources, cascades_dict):
#   cascade_ids = cascades_dict["id"] # cascade ids
#   cascade_probs = cascades_dict["proba"] # is a (given) probability distribution over the cascades (events).
#
#   statuses = []
#   penalty_reduction = 0
#   for idx, cascade_i in enumerate(cascade_ids):
#     cascade_prob = cascade_probs[idx]
#     results = [dict_outbreak_detection_binary[source][cascade_i] for source in sources]
#     detection_status = max(results) # 0: outbreak not detected, 1: outbreak detected
#     statuses.append(detection_status)
#     penalty_reduction = penalty_reduction + cascade_prob*(1 - (1 - detection_status))
#   return(penalty_reduction)


# ------------------------------------------------------------------


# def compute_min_detection_time(graph, source, target):
#   path = nx.dijkstra_path(graph, source, target, weight='weight')
#   sum = 0
#   for i in range(1,len(path)):
#     source = path[i-1]
#     target = path[i]
#     sum = sum + graph[source][target]["weight"]
#   return(sum)


def create_dict_outbreak_detection_time(graph, cascades_dict):
  cascade_ids = cascades_dict["id"] 
  
  # init
  dict_outbreak_detection_time = {}
  for node, attr_dict in graph.nodes(data=True):
    source = attr_dict["source"]
    for cascade_i in cascade_ids:
      if source not in dict_outbreak_detection_time:
        dict_outbreak_detection_time[source] = {}
      dict_outbreak_detection_time[source][cascade_i] = T_MAX
  
  S = divide_into_cascade_subgraphs(graph, cascades_dict)
  
  # for nid in [1104,7778,8036,4836,6887,1736,2122,2015]:
  #   print(graph.nodes(data=True)[nid])
  # sdf()
  
  for subgraph in S:
    # init
    processed = {}
    for node, atrr_dict in subgraph.nodes(data=True):
      source = atrr_dict["source"]
      processed[source] = False
      
    # get the cascade id from the first node
    cascade_i = -1
    for node, attr_dict in subgraph.nodes(data=True):
      cascade_i = attr_dict["cluster"]
      break
    
    sorted_nodes_of_subgraph = sorted(subgraph.nodes(data=True), key=lambda x: Temporality(x[1]["date"]).date, reverse=False)
    # each node object is a tuple with 2 elements: 1st element: node id, 2nd element: node attrs
    cascade_starting_node_obj = sorted_nodes_of_subgraph[0]
    cascade_starting_node = cascade_starting_node_obj[0]
    
    print("subgraph", subgraph.nodes(data=True))
    print("cascade_starting_node", cascade_starting_node)
    source = subgraph.nodes[cascade_starting_node]["source"]
    dict_outbreak_detection_time[source][cascade_i] = 0
    processed[source] = True
    
    # TODO: (pred,length)=nx.dijkstra_predecessor_and_distance(graph,'p64',weight="weight")
    
    #q = queue.Queue()
    #q.put(cascade_starting_node)
    #prev_nodes = []
    #while not q.empty():
    prev_node_obj = cascade_starting_node_obj
    prev_node = cascade_starting_node
    t_prev = Temporality(prev_node_obj[1]["date"]).date
    for node_obj in sorted_nodes_of_subgraph[1:]:
      node = node_obj[0]
      t = Temporality(node_obj[1]["date"]).date
      #prev_node = q.get()
      #prev_nodes.append(prev_node)
      prev_source = subgraph.nodes[prev_node]["source"]
      #for node in graph.predecessors(prev_node):
      #for node in subgraph.predecessors(prev_node):
        #if node not in prev_nodes:
        #q.put(node)
      print("--", node, graph[node])
      source = subgraph.nodes[node]["source"]
      #time = graph[node][prev_node]["weight"]
      time_diff = (t - t_prev).days
      #time = subgraph[node][prev_node]["weight"]
      # Warning: here we suppose that we dont have multiple posts of the same source
      # TODO: is it true ?
      detection_time = dict_outbreak_detection_time[prev_source][cascade_i] + time_diff
      if not processed[source]:
        dict_outbreak_detection_time[source][cascade_i] = detection_time
        processed[source] = True
      else:
        if dict_outbreak_detection_time[source][cascade_i]>detection_time:
          dict_outbreak_detection_time[source][cascade_i] = detection_time
      #
      prev_node_obj = node_obj
      prev_node = node
      t_prev = Temporality(prev_node_obj[1]["date"]).date
  return(dict_outbreak_detection_time)



# def lookup_outbreak_detection_time(dict_outbreak_detection_time, source, cascade):
#   return(dict_outbreak_detection_time[source][cascade])


def penalty_reduction_detection_time(dict_outbreak_detection_time, sources, cascades_dict):
  cascade_ids = cascades_dict["id"] # cascade ids
  cascade_probs = cascades_dict["proba"] # is a (given) probability distribution over the cascades (events).
  
  penalty_reduction = 0
  times = []
  for idx, cascade_i in enumerate(cascade_ids):
    cascade_prob = cascade_probs[idx]
    results = [dict_outbreak_detection_time[source][cascade_i] for source in sources]
    min_detection_time = min(results) # min detection time >> it can be Inf
    curr_penalty_reduction = T_MAX - min(min_detection_time,T_MAX)
    normalized_curr_penalty_reduction = curr_penalty_reduction/T_MAX
    penalty_reduction = penalty_reduction + cascade_prob*normalized_curr_penalty_reduction
  return(penalty_reduction)


# ------------------------------------------------------------------


# def create_dict_outbreak_population_affected(graph, cascades_dict):
#   cascade_ids = cascades_dict["id"] 
#   cascade_sizes = cascades_dict["nb_distinct_sources"]
#
#   # init
#   dict_outbreak_population_affected = {}
#   for node, attr_dict in graph.nodes(data=True):
#     source = attr_dict["source"]
#     for idx, cascade_i in enumerate(cascade_ids):
#       if source not in dict_outbreak_population_affected:
#         dict_outbreak_population_affected[source] = {}
#       dict_outbreak_population_affected[source][cascade_i] = cascade_sizes[idx]
#
#   S = divide_into_cascade_subgraphs(graph, cascades_dict)
#
#   for subgraph in S:
#     # init
#     processed = {}
#     for node, atrr_dict in subgraph.nodes(data=True):
#       source = atrr_dict["source"]
#       processed[source] = False
#
#     # get the cascade id from the first node
#     cascade_i = -1
#     for node, attr_dict in subgraph.nodes(data=True):
#       cascade_i = attr_dict["cluster"]
#       break
#
#     cascade_starting_node = identify_cascade_starting_node(subgraph)
#     source = subgraph.nodes[cascade_starting_node]["source"]
#     dict_outbreak_population_affected[source][cascade_i] = 0
#     processed[source] = True
#
#     # TODO: (pred,length)=nx.dijkstra_predecessor_and_distance(graph,'p64',weight="weight")
#
#     q = queue.Queue()
#     q.put(cascade_starting_node)
#     while not q.empty():
#       prev_node = q.get()
#       prev_source = subgraph.nodes[prev_node]["source"]
#       for node in graph.predecessors(prev_node):
#         q.put(node)
#         source = subgraph.nodes[node]["source"]
#         nb_sources = dict_outbreak_population_affected[prev_source][cascade_i]
#         if source != prev_source:
#           nb_sources = nb_sources + 1
#         # Warning: here we suppose that we dont have multiple posts of the same source
#         # TODO: is it true ?
#         if not processed[source]:
#           dict_outbreak_population_affected[source][cascade_i] = nb_sources
#           processed[source] = True
#   return(dict_outbreak_population_affected)




# def lookup_outbreak_population_affected(dict_outbreak_population_affected, source, cascade):
#   return(dict_outbreak_population_affected[source][cascade])


# def penalty_reduction_population_affected(dict_outbreak_population_affected, sources, cascades_dict):
#   cascade_ids = cascades_dict["id"] # cascade ids
#   cascade_sizes = cascades_dict["nb_distinct_sources"] # for each cascade i, number of distinct sources participating in cascade i
#   cascade_probs = cascades_dict["proba"] # is a (given) probability distribution over the cascades (events).
#
#   participations = []
#   penalty_reduction = 0
#   for idx, cascade_i in enumerate(cascade_ids):
#     cascade_prob = cascade_probs[idx]
#     cascade_size = cascade_sizes[idx]
#     results = [dict_outbreak_population_affected[source][cascade_i] for source in sources]
#     nb_node_outbreak_participation = min(results) # number of blogs participating in cascade
#     participations.append(nb_node_outbreak_participation)
#     curr_penalty_reduction = (cascade_size - nb_node_outbreak_participation)
#     normalized_curr_penalty_reduction = curr_penalty_reduction/cascade_size
#     penalty_reduction = penalty_reduction + cascade_prob*normalized_curr_penalty_reduction
#   return(penalty_reduction)
#
#
#
# # ------------------------------------------------------------------
#
# def create_dict_outbreak_detection_country_mention(graph, cascades_dict):
#   cascade_ids = cascades_dict["id"] 
#
#   # init
#   dict_outbreak_detection_country_mention = {}
#   for node, attr_dict in graph.nodes(data=True):
#     source = attr_dict["source"]
#     for cascade_i in cascade_ids:
#       if source not in dict_outbreak_detection_country_mention:
#         dict_outbreak_detection_country_mention[source] = {}
#       dict_outbreak_detection_country_mention[source][cascade_i] = "None"
#
#
#   S = divide_into_cascade_subgraphs(graph, cascades_dict)
#
#   for subgraph in S:
#     # get the cascade id from the first node
#     cascade_i = -1
#     for node, attr_dict in subgraph.nodes(data=True):
#       cascade_i = attr_dict["cluster"]
#       break
#
#     cascade_starting_node = identify_cascade_starting_node(subgraph)
#
#     # iterate over the nodes of the subgraph
#     for node, attr_dict in subgraph.nodes(data=True):
#       source = attr_dict["source"]
#       dict_outbreak_detection_country_mention[source][cascade_i] = attr_dict["country_mention"]
#   return(dict_outbreak_detection_country_mention)
#
#
# # def lookup_outbreak_country_mention(dict_outbreak_detection_country_mention, source, cascade):
# #   return(dict_outbreak_detection_country_mention[source][cascade])
#
#
# def penalty_reduction_detection_country_mention(dict_outbreak_detection_country_mention, sources, cascades_dict):
#   cascade_ids = cascades_dict["id"] # cascade ids
#
#   mention_countries = []
#   for idx, cascade_i in enumerate(cascade_ids):
#     curr_mention_countries = [dict_outbreak_detection_country_mention[source][cascade_i] for source in sources]
#     for curr_mention_country in curr_mention_countries:
#       if curr_mention_country not in mention_countries and curr_mention_country != str(None):
#         mention_countries.append(curr_mention_country)
#   fraction_mention_countries = len(mention_countries)/cascades_dict["nb_distinct_mention_countries"]
#   penalty_reduction = fraction_mention_countries
#   return(penalty_reduction)


# ------------------------------------------------------------------


  
def celf(graph, k, penalty_reduction_function_list, function_weight_list, penalty_reduction_data_dict_list, cascades_dict):
  """
  Find k nodes with the largest spread (determined by IC) from a networkx graph
  using the Cost Effective Lazy Forward Algorithm, a.k.a Lazy Greedy Algorithm.
  """
  #start_time = time.time()
  
  sources = list(penalty_reduction_data_dict_list[0].keys())

  # find the first node with greedy algorithm:
  # python's heap is a min-heap, thus
  # we negate the spread to get the node
  # with the maximum spread when popping from the heap
  gains = []
  for node in sources:
    final_penalty_reduction = 0
    for idx, penalty_reduction_function in enumerate(penalty_reduction_function_list):
      penalty_reduction = penalty_reduction_function(penalty_reduction_data_dict_list[idx], [node], cascades_dict)
      final_penalty_reduction = final_penalty_reduction + penalty_reduction*function_weight_list[idx]
    heapq.heappush(gains, (-final_penalty_reduction, node))

  # we pop the heap to get the node with the best spread,
  # when storing the spread to negate it again to store the actual spread
  penalty_reduction, node = heapq.heappop(gains)
  solution = [node]
  penalty_reduction = -penalty_reduction
  penalty_reductions = [penalty_reduction]

  # record the number of times the spread is computed
  #lookups = [len(sources)]
  #elapsed = [round(time.time() - start_time, 3)]

  for _ in range(k - 1):
    node_lookup = 0
    matched = False
    
    if penalty_reductions[-1]>0.99:
      break

    while not matched:
      node_lookup += 1

      # here we need to compute the marginal gain of adding the current node
      # to the solution, instead of just the gain, i.e. we need to subtract
      # the spread without adding the current node
      _, current_node = heapq.heappop(gains)
      
      final_penalty_reduction_gain = 0
      for idx, penalty_reduction_function in enumerate(penalty_reduction_function_list):
        penalty_reduction_gain = penalty_reduction_function(penalty_reduction_data_dict_list[idx], solution + [current_node], cascades_dict)
        final_penalty_reduction_gain = final_penalty_reduction_gain + penalty_reduction_gain*function_weight_list[idx]
      final_penalty_reduction_marginal_gain = final_penalty_reduction_gain - penalty_reduction
 
      # check if the previous top node stayed on the top after pushing
      # the marginal gain to the heap
      heapq.heappush(gains, (-final_penalty_reduction_marginal_gain, current_node))
      matched = gains[0][1] == current_node

    # spread stores the cumulative spread
    penalty_reduction_marginal_gain, node = heapq.heappop(gains)
    penalty_reduction -= penalty_reduction_marginal_gain
    solution.append(node)
    penalty_reductions.append(penalty_reduction)
    #lookups.append(node_lookup)

    #elapse = round(time.time() - start_time, 3)
    #elapsed.append(elapse)

  # penalty_reduction_function(penalty_reduction_data_dict, solution, cascades_dict)
  return solution, penalty_reductions




# def celf_detection_likelihood(graph, k):
#   cascades_dict = create_cascades_dict(graph)
#   #print(cascades_dict)
#   dict_outbreak_detection_binary = create_dict_outbreak_detection_binary(graph, cascades_dict)
#   #print(dict_outbreak_detection_binary)
#   result = celf(graph, k, [penalty_reduction_detection_likelihood], [1], [dict_outbreak_detection_binary], cascades_dict)
#   return(result)


def celf_detection_time(graph, k):
  cascades_dict = create_cascades_dict(graph)
  print(cascades_dict)
  dict_outbreak_detection_time = create_dict_outbreak_detection_time(graph, cascades_dict)
  #print(dict_outbreak_detection_time)
  result = celf(graph, k, [penalty_reduction_detection_time], [1], [dict_outbreak_detection_time], cascades_dict)
  return(result)


# def celf_population_affected(graph, k):
#   cascades_dict = create_cascades_dict(graph)
#   #print(cascades_dict)
#   dict_outbreak_population_affected = create_dict_outbreak_population_affected(graph, cascades_dict)
#   #print(dict_outbreak_population_affected)
#   result = celf(graph, k, [penalty_reduction_population_affected], [1], [dict_outbreak_population_affected], cascades_dict)
#   return(result)
#
#
# def celf_mention_country(graph, k):
#   cascades_dict = create_cascades_dict(graph)
#   #print(cascades_dict)
#   dict_outbreak_detection_country_mention = create_dict_outbreak_detection_country_mention(graph, cascades_dict)
#   #print(dict_outbreak_population_affected)
#   result = celf(graph, k, [penalty_reduction_detection_country_mention], [1], [dict_outbreak_detection_country_mention], cascades_dict)
#   return(result)
#
#
# def celf_detection_likelihood_and_detection_time(graph, k):
#   cascades_dict = create_cascades_dict(graph)
#   #print(cascades_dict)
#   dict_outbreak_detection_binary = create_dict_outbreak_detection_binary(graph, cascades_dict)
#   dict_outbreak_detection_time = create_dict_outbreak_detection_time(graph, cascades_dict)
#   #print(dict_outbreak_detection_time)
#   result = celf(graph, k, [penalty_reduction_detection_likelihood,penalty_reduction_detection_time], [0.5,0.5], [dict_outbreak_detection_binary,dict_outbreak_detection_time], cascades_dict)
#   return(result)
#
#
# def celf_detection_likelihood_and_detection_time_mention_country(graph, k):
#   cascades_dict = create_cascades_dict(graph)
#   #print(cascades_dict)
#   dict_outbreak_detection_binary = create_dict_outbreak_detection_binary(graph, cascades_dict)
#   dict_outbreak_detection_time = create_dict_outbreak_detection_time(graph, cascades_dict)
#   dict_outbreak_detection_country_mention = create_dict_outbreak_detection_country_mention(graph, cascades_dict)
#   #print(dict_outbreak_detection_time)
#   result = celf(graph, k, [penalty_reduction_detection_likelihood,penalty_reduction_detection_time,penalty_reduction_detection_country_mention], [0.33,0.33,0.33], [dict_outbreak_detection_binary,dict_outbreak_detection_time, dict_outbreak_detection_country_mention], cascades_dict)
#   return(result)


