'''
Created on Sep 1, 2022

@author: nejat
'''




from math import radians, cos, sin, asin, sqrt
import pycountry_convert as pc


       
# https://stackoverflow.com/questions/15736995/how-can-i-quickly-estimate-the-distance-between-two-latitude-longitude-points
def haversine(lon1, lat1, lon2, lat2):
  """
  Calculate the great circle distance between two points 
  on the earth (specified in decimal degrees)
  """
  # convert decimal degrees to radians 
  lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
  # haversine formula 
  dlon = lon2 - lon1 
  dlat = lat2 - lat1 
  a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
  c = 2 * asin(sqrt(a)) 
  # Radius of earth in kilometers is 6371
  km = 6371* c
  return km
  
  
  
def retrieve_country_alpha2_code_from_alpha3_code(alpha3_code):
  if alpha3_code == "-1":
    return "-1"
  elif alpha3_code == "XKO":
    return "XK"
  else:
   return pc.country_alpha3_to_country_alpha2(alpha3_code)
  
  
def retrieve_continent_from_country_code(country_code):
  #
  continent_name = ""
  try:
    if len(country_code) == 3: # alpha3
      country_code = pc.country_alpha3_to_country_alpha2(country_code)
    continent_name = pc.country_alpha2_to_continent_code(country_code)
  except KeyError:
    print(country_code, "is a key error")
  return continent_name



def retrieve_shapefile_country_id_from_country_alpha2_code(country_code, map_data):
  row = map_data[map_data["isocode"] == country_code]
  id = row["ID"].to_list()[0]
  return id


