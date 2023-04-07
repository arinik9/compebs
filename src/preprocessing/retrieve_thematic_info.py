# '''
# Created on Nov 29, 2022
#
# @author: nejat
# '''
#
# import pandas as pd
# import consts
# import os
# import csv
#
#
#
# def retrieve_all_disease_info(all_disease_info_dict):
#   df_list = []
#   for disease, disease_info_list in all_disease_info_dict.items():
#     disease_item_hier_dict = {}
#     # an item of "disease_info_list": {"text": "h5n6", "level": 3, "hierarchy": ("AI", "hpai", "h5n6")}
#     for item_dict in disease_info_list:
#       lvl = item_dict["level"]
#       txt = item_dict["hierarchy"][lvl-1]
#       if "unknown" in txt:
#         lvl = 1
#       if txt == "hpai" or txt == "lpai":
#         txt = txt.upper()
#       disease_item_hier_dict[txt] = lvl
#     df = pd.DataFrame({"disease": disease, "text": disease_item_hier_dict.keys(), "hier_level": disease_item_hier_dict.values()})
#     df_list.append(df)
#   df = pd.concat(df_list)
#   return(df)
#
#
# def retrieve_all_host_info(all_host_info_dict):
#   df_list = []
#   for host, host_info_list in all_host_info_dict.items():
#     host_item_hier_dict = {}
#     # an item of "disease_info_list": {"text": "house crow", "level": 2, "hierarchy":("domestic bird", "crow")},
#     for item_dict in host_info_list:
#       lvl = item_dict["level"]
#       txt = ""
#       if host == "avian":
#         if lvl == 0 or lvl == 1:
#           txt = item_dict["hierarchy"][0]
#         else:
#           txt = item_dict["hierarchy"][1]
#       else:
#         txt = item_dict["hierarchy"][lvl]
#       lvl += 1
#       host_item_hier_dict[txt] = lvl
#     df = pd.DataFrame({"host": host, "text": host_item_hier_dict.keys(), "hier_level": host_item_hier_dict.values()})
#     df_list.append(df)
#   df = pd.concat(df_list)
#   return(df)
#
#
#
# def retrieve_all_host_and_disease_info(out_preprocessing_folder, force):
#   try:
#     if not os.path.exists(out_preprocessing_folder):
#       os.makedirs(out_preprocessing_folder)
#   except OSError as err:
#     print(err)
#
#   host_result_filepath = os.path.join(out_preprocessing_folder, "host_info.csv")
#   disease_result_filepath = os.path.join(out_preprocessing_folder, "disease_info.csv")
#   if (not os.path.exists(host_result_filepath) or not os.path.exists(disease_result_filepath)) or force:
#
#     # disease
#     all_disease_info_dict = consts.DISEASE_KEYWORDS_HIERARCHY_DICT
#     df = retrieve_all_disease_info(all_disease_info_dict)
#
#     df.to_csv(disease_result_filepath, sep=";", quoting=csv.QUOTE_NONNUMERIC)
#
#     # host
#     all_host_info_dict = consts.HOST_KEYWORDS_HIERARCHY_DICT
#     df = retrieve_all_host_info(all_host_info_dict)
#     df.to_csv(host_result_filepath, sep=";", quoting=csv.QUOTE_NONNUMERIC)
#
#
#
