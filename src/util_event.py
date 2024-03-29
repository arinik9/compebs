'''
Created on Sep 16, 2022

@author: nejat
'''

import consts
import os
import pandas as pd

import json

from event.event import Event
from event.location import Location
from event.temporality import Temporality
from event.host import Host
from event.disease import Disease
from event.symptom import Symptom

from iso3166 import countries
import csv
import dateutil.parser as parser




def read_df_events(events_filepath):
  cols_events = [consts.COL_ID, consts.COL_ARTICLE_ID, consts.COL_URL, consts.COL_SOURCE, \
                    consts.COL_GEONAMES_ID, "geoname_json", "loc_name", "loc_country_code", consts.COL_LOC_CONTINENT, \
                    consts.COL_LAT, consts.COL_LNG, "hierarchy_data", consts.COL_PUBLISHED_TIME, consts.COL_DISEASE,  \
                   consts.COL_HOST, \
                   #consts.COL_SYMPTOM_SUBTYPE, consts.COL_SYMPTOM, \
                   # consts.COL_TITLE, consts.COL_SENTENCES, \
                    "day_no", "week_no", "month_no", "month_no", "year", "season"
                   ]
  df_events = pd.read_csv(events_filepath, usecols=cols_events, sep=";", keep_default_na=False)
  df_events[consts.COL_PUBLISHED_TIME] = df_events[consts.COL_PUBLISHED_TIME].apply(lambda x: parser.parse(x))
  
  df_events = df_events.rename(columns={"month_no": "month_no_simple"})
  df_events = df_events.rename(columns={"week_no": "week_no_simple"})
  df_events["month_no"] = df_events["month_no_simple"].apply(str) + "_" + df_events["year"].apply(str)
  df_events["week_no"] = df_events["week_no_simple"].apply(str) + "_" + df_events["year"].apply(str)
  df_events["season_no_simple"] = df_events["season"].replace(["winter", "spring", "summer", "autumn"], [1, 2, 3, 4])
  df_events["season_no"] = df_events["season_no_simple"].apply(str) + "_" + df_events["year"].apply(str)
  return df_events


def read_events_from_df(df_events, in_taxonomy_folder):
  
  # df_events = read_df_events(events_filepath)
  
  #
  disease_info_filepath = os.path.join(in_taxonomy_folder, "disease_info.csv")
  df_disease_info = pd.read_csv(disease_info_filepath, sep=";", keep_default_na=False)
  disease_text_to_disease = dict(zip(df_disease_info["text"], df_disease_info["disease"]))
  disease_text_to_hier_level = dict(zip(df_disease_info["text"], df_disease_info["hier_level"]))
  #
  host_info_filepath = os.path.join(in_taxonomy_folder, "host_info.csv")
  df_host_info = pd.read_csv(host_info_filepath, sep=";", keep_default_na=False)
  host_text_to_host = dict(zip(df_host_info["text"], df_host_info["host"]))
  host_text_to_hier_level = dict(zip(df_host_info["text"], df_host_info["hier_level"]))
  
  events = []
  for index, row in df_events.iterrows():
    loc = Location(row["loc_name"], row[consts.COL_GEONAMES_ID], json.loads(row["geoname_json"]), \
                   row[consts.COL_LAT], row[consts.COL_LNG], row["loc_country_code"], row[consts.COL_LOC_CONTINENT], \
                   eval(row["hierarchy_data"]))
    t = Temporality(row[consts.COL_PUBLISHED_TIME], row["day_no"], row["week_no"], row["month_no"], row["year"], row["season"], row["season_no"])
    disease_tuple = eval(row[consts.COL_DISEASE])
    dis = Disease(disease_tuple[0], disease_tuple[1])
    dis_text = disease_tuple[0]
    if dis_text == "":
      dis_text = disease_tuple[1]
    d_lvl = disease_text_to_hier_level[dis_text]
    dis.set_max_hierarchy_level(d_lvl)
    #print(dis_text, d_lvl)
    h = Host(json.loads(row[consts.COL_HOST]))
    h_vals = h.get_unnested_entry() # [('domestic bird', ['chicken', 'turkey'])] OR [('bird-unknown', ['subtype-unknown'])]
    h_texts = [h_val[-1][0] if "unknown" not in h_val[-1][0] else h_val[-2] for h_val in h_vals ]
    h_lvl = min([host_text_to_hier_level[h_text] for h_text in h_texts])
    #print(h_texts, h_lvl)
    h.set_max_hierarchy_level(h_lvl)
    sym = Symptom()
    # sym.load_dict_data_from_str(row[consts.COL_SYMPTOM_SUBTYPE], row[consts.COL_SYMPTOM])
    e = Event(int(row[consts.COL_ID]), row[consts.COL_ARTICLE_ID], row[consts.COL_URL], \
                    row[consts.COL_SOURCE], loc, t, dis, h, sym, "", "")
    events.append(e)
    
  return events




def get_event_clusters_from_clustering_result(clustering_filepath, events):
  id_to_event = {}
  for e in events:
    id_to_event[int(e.e_id)] = e
      
  res_event_clustering = pd.read_csv(clustering_filepath, header=None)[0]
  clusters = []
  for grouping_info_str in res_event_clustering:
    e_list = [id_to_event[int(grouping_info_str.split(",")[0])]] # a single event
    if "," in grouping_info_str: # for more than one event
      e_list = [id_to_event[int(id)] for id in grouping_info_str.split(",")]
    clusters.append(e_list)
  return(clusters)


def simplify_df_events_at_hier_level1(events_filepath, new_events_filepath=None):
  df_events = read_df_events(events_filepath)
  
  country_code_list = []
  country_name_list = []
  for index, country_code in enumerate(df_events["loc_country_code"].to_list()):
    country_code_alpha2 = countries.get(country_code).alpha2
    country_code_list.append(country_code_alpha2)
    
    country_name = countries.get(country_code).name
    if country_code == "KOR":
      country_name = "South Korea"
    if country_code == "PRK":
      country_name = "North Korea"
    if country_code == "IRN":
      country_name = "Iran"
    if country_code == "GBR":
      country_name = "United Kingdom"
    if country_code == "USA":
      country_name = "United States"
    if country_code == "TWN":
      country_name = "Taiwan"
    if country_code == "RUS":
      country_name = "Russia"
    if country_code == "LAO":
      country_name = "Laon"
    country_name_list.append(country_name)
    
  region_name_list = []
  for index, geoname_json_str in enumerate(df_events["geoname_json"].to_list()):
    geoname_json = json.loads(geoname_json_str)
    region_name = ""
    if "adminName1" in geoname_json:
      region_name = geoname_json["adminName1"]
    region_name_list.append(region_name)
    
  city_name_list = []
  for index, geoname_json_str in enumerate(df_events["geoname_json"].to_list()):
    geoname_json = json.loads(geoname_json_str)
    #print(geoname_json)
    fcode = None
    if "fcode" in geoname_json:
      fcode = geoname_json["fcode"]
    if "code" in geoname_json:
      fcode = geoname_json["code"]
    if fcode is not None and fcode != "ADM1" and fcode != "PCLI" and fcode != "PCLS":
      city_name = geoname_json["toponymName"]
      city_name_list.append(city_name)
    else:
      city_name_list.append("")
      
  disease_name_list = []
  disease_subtype_list = []
  for index, diseae_info_str in enumerate(df_events["disease"].to_list()):
    diseae_info = eval(diseae_info_str)
    disease_name = diseae_info[1]
    disease_name_list.append(disease_name)
    disease_subtype = diseae_info[0]
    disease_subtype_list.append(disease_subtype)
    
  host_name_list = []
  host_subtype_list = []
  for index, host_info_str in enumerate(df_events["host"].to_list()):
    host_info = json.loads(host_info_str)
    host_info_keys = list(host_info.keys())
    if len(host_info_keys) == 1 and host_info_keys[0] == "human":
      host_name_list.append(host_info_keys[0])
      host_subtype_list.append(",".join(host_info["human"]))
    elif len(host_info_keys) == 1 and host_info_keys[0] == "mosquito":
      host_name_list.append(host_info_keys[0])
      host_subtype_list.append(",".join(host_info["mosquito"]))
    elif len(host_info_keys) == 1 and host_info_keys[0] in ["equidae", "arctoidea", "canidae", "camelidae"]:
      host_name_list.append("mammal")
      host_subtype_list.append(host_info_keys[0])
    else:
      host_name_list.append("bird")
      host_subtype_list.append(",".join(host_info_keys))

  data = {"country_code":country_code_list, "country": country_name_list, "region": region_name_list, "locality": city_name_list, \
           "disease": disease_name_list, "disease subtype": disease_subtype_list,\
            "host": host_name_list, "host subtype": host_subtype_list}
  data["id"] = df_events["id"].to_list()
  data["article_id"] = df_events["article_id"].to_list()
  data["url"] = df_events["url"].to_list()
  data["source"] = df_events["source"].to_list()
  data["continent"] = df_events["continent"].to_list()
  data["geonames_id"] = df_events["geonames_id"].to_list()
  data["lat"] = df_events["lat"].to_list()
  data["lng"] = df_events["lng"].to_list()
  data["published_at"] = df_events["published_at"].to_list()
  #data["symptom"] = df_events["symptom"].to_list()
  #data["symptom subtype"] = df_events["symptom subtype"].to_list()
  #data["title"] = df_events["title"].to_list()
  #data["sentences"] = df_events["sentences"].to_list()
  data["day_no"] = df_events["day_no"].to_list()
  data["week_no"] = df_events["week_no"].to_list()
  data["week_no_simple"] = df_events["week_no"].apply(lambda x: int(x.split("_")[0])).to_list()
  data["month_no"] = df_events["month_no"].to_list()
  data["month_no_simple"] = df_events["month_no"].apply(lambda x: int(x.split("_")[0])).to_list()
  data["year"] = df_events["year"].to_list()
  data["season"] = df_events["season"].to_list()
  df = pd.DataFrame(data)
  
  if new_events_filepath is not None:
    print(new_events_filepath)
    df.to_csv(new_events_filepath, sep=";", quoting=csv.QUOTE_NONNUMERIC)
  return(df)

