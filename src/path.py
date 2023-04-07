'''
Created on Nov 16, 2021

@author: nejat
'''

import os


def get_event_distribution_folder_path(output_dirpath, EI_platform="", continent="", season="", year=""):
  return get_spatiotemporal_custom_folder_path(output_dirpath, EI_platform, continent, season, year)
  
  
  
def get_spatiotemporal_custom_folder_path(output_dirpath, EI_platform="", continent="", season="", year="",\
                                           spatial_scale="", temporal_scale=""):
  output_dirpath = output_dirpath.replace("<PLATFORM>", EI_platform)
  
  desc = ""
  if continent != "":
    desc = desc + "continent="+continent
  if year != "":
    if desc != "":
      desc = desc + "_"
    desc = desc + "season="+season
  if year != "":
    if desc != "":
      desc = desc + "_"
    desc = desc + "year="+str(year)   
    
  if spatial_scale != "":
    if desc != "":
      desc = desc + "_"
    desc = desc + "Z="+spatial_scale 
    
  if temporal_scale != "":
    if desc != "":
      desc = desc + "_"
    desc = desc + "T="+temporal_scale 
    
  if desc != "":
    output_dirpath = os.path.join(output_dirpath, desc)
  return output_dirpath


    
