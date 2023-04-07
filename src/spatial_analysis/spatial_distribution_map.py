'''
Created on Sep 18, 2022

@author: nejat
'''

from plot.plot_event_distribution import prepare_all_event_distributions, plot_all_event_distributions, plot_all_event_comparison_maps


def perform_spatial_distribution_map(in_taxonomy_folder, input_shapefile_folder, events_filepath_dict, output_dirpath, by_continent):
  
  #spatial_hierarchy_levels = ["country", "region", "city"]
  #spatial_hierarchy_levels = ["region"]
  spatial_hierarchy_levels = ["country", "region"] # 
  # no restriction on plot max limit value, so put all spatial hierarchy values
  periods = ["All"]
  seasons = ["All"]
  #periods = [2020, 2021] # 
  #seasons = ["summer", "spring", "autumn", "winter"] #  
  prepare_all_event_distributions(in_taxonomy_folder, input_shapefile_folder, events_filepath_dict, output_dirpath, by_continent, seasons, periods, spatial_hierarchy_levels)
  plot_all_event_distributions(list(events_filepath_dict.keys()), output_dirpath, by_continent, seasons, periods, spatial_hierarchy_levels)
  plot_all_event_comparison_maps(list(events_filepath_dict.keys()), output_dirpath, by_continent, seasons, periods, spatial_hierarchy_levels)
  
