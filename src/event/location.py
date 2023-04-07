'''
Created on Nov 14, 2021

@author: nejat
'''

import json


class Location:

  def __init__(self, name, geoname_id, geoname_json, lat, lng, country_code, continent, hierarchy_data):
    self.name = name
    self.geoname_id = geoname_id
    self.geoname_json = geoname_json
    self.lat = lat
    self.lng = lng
    self.country_code = country_code
    self.continent = continent
    self.hierarchy_data = hierarchy_data # it is a list of geoname ids from country level to current level
    self.hierarchy_level = len(hierarchy_data)-1 # country level is level 0, ...
    

  def get_name(self):
    return self.name
  
  def get_geoname_id(self):
    return self.geoname_id
  
  def get_lat_lng(self):
    return self.lat, self.lng

  def get_country_code(self):
    return self.country_code

  def get_continent(self):
    return self.continent

  def get_hierarchy_level(self):
    return self.hierarchy_level
    
  def get_hierarchy_data(self):
    return self.hierarchy_data
  
  def is_country(self):
    if len(self.hierarchy_data) == 1 and self.hierarchy_data[0] == self.geoname_id:
      return True
    return False
    
  #
  # def set_geonames_id(self, gid):
  #   self.geonames_id = gid
  #
  #
  # def set_lat_lng(self, lat, lng):
  #   self.lat = lat
  #   self.lng = lng
      
      
  def get_entry(self):
    return([self.geoname_id, json.dumps(self.geoname_json), self.name, self.country_code, self.continent, self.lat, self.lng, json.dumps(self.hierarchy_data)])


  def is_spatially_included(self, another_loc):
    if self.country_code == another_loc.country_code:
      if another_loc.hierarchy_level < self.hierarchy_level: # e.g. level 1 < level 3
        if self.hierarchy_data[0:(another_loc.hierarchy_level+1)] == another_loc.hierarchy_data:
          return True
    return False
  

  def spatially_contains(self, another_loc):
    if self.country_code == another_loc.country_code:
      if self.hierarchy_level < another_loc.hierarchy_level: # e.g. level 1 < level 3
        if another_loc.hierarchy_data[0:(self.hierarchy_level+1)] == self.hierarchy_data:
          return True
    return False
  
  def is_identical(self, another_loc):
    if self.get_geoname_id() == another_loc.get_geoname_id():
      return True
    return False
  
  
  # # we stick to the country info in loc1. We just try to get extra information from loc2
  # def extend_location_from_another_event_if_possible(self, loc2):
  #   #loc1 = Location(self.city, self.region, self.country)
  #   #print(self.country, loc2.country)
  #   update = False
  #   if self.continent != "" and self.continent == loc2.continent and  self.country != "" and self.country == loc2.country:
  #     if self.region == "" and loc2.region != "" and loc2.region != loc2.country:
  #       self.region = loc2.region
  #       update = True
  #     elif self.region != "" and self.region == loc2.region:
  #       if self.city == "" and loc2.city != "":
  #         self.city = loc2.city
  #         update = True
  #   elif self.continent != "" and self.continent == loc2.continent and self.country == "" and loc2.country != "":
  #     print("Error in extend_location_from_another_event_if_possible()")
  #     self.country = loc2.country
  #     self.region = loc2.region
  #     self.city = loc2.city
  #     update = True
  #
  #   if update:
  #     self.set_geonames_id(loc2.get_geonames_id())
  #
  #   #return(loc1)
    
  
  def __repr__(self):
    return "[" + str(self.geoname_id) + "," +  self.name + "," +  self.country_code + "," + str(self.continent) \
       + "," + str(self.lat) + "," + str(self.lng) +  "]"
       
  def __str__(self):
    return "[" + str(self.geoname_id) + "," +  str(self.name) + "," +  str(self.country_code) + "," + str(self.continent) \
       + "," + str(self.lat) + "," + str(self.lng) +  "]"
  
  
     