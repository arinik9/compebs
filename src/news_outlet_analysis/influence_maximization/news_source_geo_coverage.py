'''
Created on Dec 15, 2021

@author: nejat
'''
import os
import pandas as pd
import consts


#import seaborn as sns; sns.set_theme() # for heatmap


from tldextract import extract
from iso3166 import countries


# http://la1ere.francetvinfo.fr/wallisfutuna/
# http://la1ere.francetvinfo.fr/guadeloupe/
# http://la1ere.francetvinfo.fr/martinique/
# http://www.lepetitjournal.com/rio-de-janeiro
# http://www.lepetitjournal.com/berlin
# http://www.lepetitjournal.com/athenes
# http://www.lepetitjournal.com/budapest
def trim_url_custom2(url):
  # print(url)
  http_count = url.count("http")
  if http_count > 0:
    url_part_by_http = url.split("http")
    part_of_interest_url = url_part_by_http[http_count]
    part_of_interest = part_of_interest_url.split("//")[1]
    twitter_count = part_of_interest.count("twitter")
    if twitter_count>0:
      # https://twitter.com/FluTrackers/statuses/1077629051630702593
      if "/status" in part_of_interest:
        part_of_interest = part_of_interest.split("/status")[0]
      else:
        part_of_interest = part_of_interest.split("/statuses")[0]
    # ---------------------------
    tsd, td, tsu = extract(part_of_interest)
    trim_url = td + "." + tsu
    if td not in ["maville"]:
      if tsd != "":
        trim_url = tsd + "." +  td + "." + tsu
      if td in ["francetvinfo", "lepetitjournal", "theguardian"]:
        part2 = url.split(trim_url+"/")[1]
        trim_url = trim_url + "/" +part2.split("/")[0]
    
    #print(url, trim_url)
    return trim_url
  # print(url, "-1")
  return "-1"   


def retrieve_country_code_from_url_public_suffix(url):
  # for more info: https://en.wikipedia.org/wiki/Country_code_top-level_domain
  tsd, td, tsu = extract(url)
  tsu = tsu.replace("co.uk", "gb")
  tsu = tsu.replace("co.", "")
  tsu = tsu.replace("com.", "")
  tsu = tsu.replace("org.", "")
  tsu = tsu.replace("or.", "")
  tsu = tsu.replace("gov.", "")
  tsu = tsu.replace("net.", "")
  if tsu == "com":
    return "-1"
  country_code = "-1"
  if tsu in countries:
    country_code = countries.get(tsu).alpha3
  return country_code
  



def create_dict_url_to_pub_country_code(in_news_websites_geo_folder):
  #country_code_filepath = os.path.join(consts.IN_NEWS_WEBSITES_GEO_FOLDER, "countries_codes_and_coordinates" + "." + consts.FILE_FORMAT_CSV)
  #cols_country_code = [consts.COL_COUNTRY, consts.COL_COUNTRY_ALPHA3_CODE]
  #df_country_code = pd.read_csv(country_code_filepath, usecols=cols_country_code, sep=",")
  #pub_country_iso_code_to_pub_country = dict(zip(df_country_code[consts.COL_COUNTRY_ALPHA3_CODE], df_country_code[consts.COL_COUNTRY]))
  
  geo_media_sources_filepath = os.path.join(in_news_websites_geo_folder, "media_sources" + "." + consts.FILE_FORMAT_CSV)
  cols_geo_media_sources = [consts.COL_URL, consts.COL_PUB_COUNTRY]
  df_geo_media_sources = pd.read_csv(geo_media_sources_filepath, usecols=cols_geo_media_sources, sep=",")
  
  new_values = []
  for pub_country_iso_code in df_geo_media_sources[consts.COL_PUB_COUNTRY]:
    name = countries.get(pub_country_iso_code).name
    new_values.append(name)
    # elif pub_country_iso_code == "SXM":
    #   new_values.append("Sint Maarten")
    # elif pub_country_iso_code == "BES":
    #   new_values.append("Bonaire, Saint Eustatius and Saba")
    # elif pub_country_iso_code == "XKX":
    #   new_values.append("Kosovo")
    # elif pub_country_iso_code == "CUW":
    #   new_values.append("Curaçao")
    # elif pub_country_iso_code == "MAF":
    #   new_values.append("Saint Martin")
    # elif pub_country_iso_code == "BLM":
    #   new_values.append("Saint Barthelemy")  
    # else:
    #   new_values.append("-1")
  df_geo_media_sources["country_name"] = new_values
  
  df_geo_media_sources[consts.COL_URL].str.replace("urn://", "http://")
  df_geo_media_sources[consts.COL_URL] = df_geo_media_sources[consts.COL_URL].apply(lambda x: "http://"+x if "http" not in x else x)
  # trim
  df_geo_media_sources[consts.COL_URL] = df_geo_media_sources[consts.COL_URL].apply(trim_url_custom2)
  
  df_media_source2 = df_geo_media_sources.groupby([consts.COL_URL])[consts.COL_PUB_COUNTRY, "country_name"].aggregate(lambda x: list(x)[0])
  geo_media_sources_filepath = os.path.join(in_news_websites_geo_folder, "media_sources_adj" + "." + consts.FILE_FORMAT_CSV)
  df_media_source2.to_csv(geo_media_sources_filepath, sep=",")
  
  source_url_to_pub_country_code = dict(zip(df_media_source2.reset_index()[consts.COL_URL], df_media_source2.reset_index()[consts.COL_PUB_COUNTRY]))
  #print(source_url_to_pub_country)
  return(source_url_to_pub_country_code)


  
