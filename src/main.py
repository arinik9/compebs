import os
import consts

from news_outlet_analysis.perform_news_outlet_analysis import perform_news_outlet_pagerank_analysis, perform_news_outlet_time_detection_analysis
from news_outlet_analysis.compute_rank_cor_news_outlets import compute_Kishida_normalized_precision_and_recall_for_news_outlets
from spatial_analysis.spatial_distribution_map import perform_spatial_distribution_map
from event_matching.event_matching import EventMatching
from event_matching.event_matching_strategy import EventMatchingStrategyEventSimilarity
from util_event import simplify_df_events_at_hier_level1
from spatial_analysis.temporal_geo_coverge import process_temporal_geo_coverage_for_all_platforms, plot_temporal_geo_coverage_results_for_all_platforms, plot_temporal_geo_coverage_result_comparison_for_all_platforms, compute_final_temporal_geo_coverage_result_comparison_for_all_platforms
from temporal_analysis.process_timeliness_analysis import plot_timeliness_for_all_platforms, compute_timeliness_for_all_platforms
from temporal_analysis.plot_event_evolution import plot_event_evolution_for_all_platforms
from thematic_analysis.plot_chord_diagram import plot_chord_diagram_for_all_platforms
from temporal_analysis import process_st_motifs
from preprocessing.retrieve_geonames_info_for_events import create_single_geonames_info_file_from_all_events
from preprocessing.get_geoname_ids_for_countries import retrieve_geonames_id_for_countries
from preprocessing.get_geoname_ids_for_regions_asap import retrieve_geonames_id_for_regions_from_asap
from preprocessing.retrieve_geonames_neighbors import create_country_neighbors_info_file
from thematic_analysis.extract_multidim_motifs import process_continuous_periodic_multidim_st_motif_extraction
from thematic_analysis.compute_rank_corr_for_multidim_motifs import compute_Kishida_normalized_precision_and_recall_for_multidim_motifs
from temporal_analysis.st_motifs.compute_rank_corr_for_st_motifs import compute_Kishida_normalized_precision_and_recall_for_continuous_periodic_st_motifs
from temporal_analysis.st_motifs.compute_temporal_geo_coverage_for_st_season_periodic_motifs import compute_temporal_geo_coverage_for_st_seasonal_periodic_motifs
from stats.collect_all_quantitative_results import retrieve_and_plot_all_quantitative_results


# ====================================================================
MAIN_FOLDER = "<YOUR_FOLDER>"

IN_FOLDER = os.path.join(MAIN_FOLDER, "in")
OUT_FOLDER = os.path.join(MAIN_FOLDER, "out")

LIB_FOLDER = os.path.join(MAIN_FOLDER, "lib")
DATA_FOLDER = os.path.join(MAIN_FOLDER, "data")
# ====================================================================





IN_EVENTS_FOLDER = os.path.join(IN_FOLDER, "events")
IN_THEMATIC_TAXONOMY_FOLDER = os.path.join(IN_FOLDER, "thematic_taxonomy")
IN_MAP_SHAPEFILE_FOLDER = os.path.join(IN_FOLDER, "map_shapefiles")
IN_GEONAMES_INFO_FOLDER = os.path.join(IN_FOLDER, "geonames")
IN_NEWS_WEBSITES_GEO_FOLDER = os.path.join(IN_FOLDER, "news_outlets_geography")
IN_MAP_SHAPEFILE_FOLDER = os.path.join(IN_FOLDER, "map_shapefiles")
IN_ENV_DATA_FOLDER = os.path.join(IN_FOLDER, "environmental_data")
DATA_SOURCE_GEO_COVERAGE_FOLDER = os.path.join(IN_FOLDER, "news_outlets_geography")

OUT_SPATIAL_ANALYSIS_FOLDER = os.path.join(OUT_FOLDER, "spatial_analysis")
OUT_TEMPORAL_ANALYSIS_FOLDER = os.path.join(OUT_FOLDER, "temporal_analysis")
OUT_ST_PATTERN_FOLDER = os.path.join(OUT_TEMPORAL_ANALYSIS_FOLDER, "st_pattern")
OUT_TIMELINESS_FOLDER = os.path.join(OUT_FOLDER, "timeliness")
OUT_THEMATIC_ANALYSIS_FOLDER = os.path.join(OUT_FOLDER, "thematic_analysis")
OUT_NEWS_OUTLET_ANALYSIS_FOLDER = os.path.join(OUT_FOLDER, "newslet_outlet_analysis")
OUT_GRAPH_FOLDER = os.path.join(OUT_FOLDER, "graph")
STATS_FOLDER = os.path.join(OUT_FOLDER, "stats")
DATAFRAME_ALIGNMENT_FOLDER = os.path.join(OUT_FOLDER, "dataframe-alignment")
OUT_PREPROCESSING_FOLDER = os.path.join(OUT_FOLDER, "preprocessing")




FORCE = False # TODO: use it systematically in every main function


if __name__ == '__main__':
  
    
  #########################################
  # EMPRES-i
  #########################################
  input_event_folder_empres_i = os.path.join(IN_EVENTS_FOLDER, consts.NEWS_DB_EMPRESS_I)

  events_filepath_empresi = os.path.join(input_event_folder_empres_i, "events.csv")
     
  events_simplified_filepath_empresi = os.path.join(input_event_folder_empres_i, "events_simplified.csv")
  simplify_df_events_at_hier_level1(events_filepath_empresi, events_simplified_filepath_empresi)
     
      
  #########################################
  # PADI-Web
  #########################################
  input_event_folder_padiweb = os.path.join(IN_EVENTS_FOLDER, consts.NEWS_SURVEILLANCE_PADIWEB)
  
  event_candidates_filepath_padiweb = os.path.join(input_event_folder_padiweb, "event_candidates.csv")
  clustering_result_filepath_padiweb = os.path.join(input_event_folder_padiweb, "event-clustering.txt")
  events_filepath_padiweb = os.path.join(input_event_folder_padiweb, "events.csv")
     
  events_simplified_filepath_padiweb = os.path.join(input_event_folder_padiweb, "events_simplified.csv")
  simplify_df_events_at_hier_level1(events_filepath_padiweb, events_simplified_filepath_padiweb)
  
  
  
  #########################################
  # ProMED
  #########################################
  input_event_folder_promed = os.path.join(IN_EVENTS_FOLDER, consts.NEWS_SURVEILLANCE_PROMED)
  
  event_candidates_filepath_promed = os.path.join(input_event_folder_promed, "event_candidates.csv")
  clustering_result_filepath_promed = os.path.join(input_event_folder_promed, "event-clustering.txt")
  events_filepath_promed = os.path.join(input_event_folder_promed, "events.csv")
  
  events_simplified_filepath_promed = os.path.join(input_event_folder_promed, "events_simplified.csv")
  simplify_df_events_at_hier_level1(events_filepath_promed, events_simplified_filepath_promed)
  
  
  #########################################
  # Event matching between the considered EBS platforms
  #  1) PADI-Web - ProMED, 2) PADI-Web - EMPRES-i, 3) ProMED - EMPRES-i
  #########################################
  output_dirpath_event_matching = os.path.join(OUT_FOLDER, "event_matching")
  try:
    if not os.path.exists(output_dirpath_event_matching):
      os.makedirs(output_dirpath_event_matching)
  except OSError as err:
    print(err)
    
    
    
    
  #########################################
  # PREPROCESSING
  #########################################
  input_shapefile_folder = IN_MAP_SHAPEFILE_FOLDER
  out_preprocessing_folder = OUT_PREPROCESSING_FOLDER
  
  create_single_geonames_info_file_from_all_events(IN_THEMATIC_TAXONOMY_FOLDER, events_filepath_padiweb, events_filepath_promed, events_filepath_empresi, out_preprocessing_folder, FORCE)
  
  retrieve_geonames_id_for_countries(input_shapefile_folder, out_preprocessing_folder, FORCE)
  retrieve_geonames_id_for_regions_from_asap(input_shapefile_folder, out_preprocessing_folder, FORCE)
  
  create_country_neighbors_info_file(out_preprocessing_folder, FORCE)
  
  
  
  

  #########################################
  # EVENT MATCHING
  ######################################### 
  
  event_matching_strategy = EventMatchingStrategyEventSimilarity()
  job_event_matching = EventMatching(event_matching_strategy)
  job_event_matching.perform_event_matching(IN_THEMATIC_TAXONOMY_FOLDER, consts.NEWS_SURVEILLANCE_PADIWEB,\
                                            events_filepath_padiweb,\
                                            consts.NEWS_SURVEILLANCE_PROMED,\
                                            events_filepath_promed,\
                                            output_dirpath_event_matching)
  
  job_event_matching.perform_event_matching(IN_THEMATIC_TAXONOMY_FOLDER, consts.NEWS_SURVEILLANCE_PADIWEB,\
                                            events_filepath_padiweb,\
                                            consts.NEWS_DB_EMPRESS_I,\
                                            events_filepath_empresi,\
                                            output_dirpath_event_matching)
  
  job_event_matching.perform_event_matching(IN_THEMATIC_TAXONOMY_FOLDER, consts.NEWS_SURVEILLANCE_PROMED,\
                                            events_filepath_promed,\
                                            consts.NEWS_DB_EMPRESS_I,\
                                            events_filepath_empresi,\
                                            output_dirpath_event_matching)
  
  
  
  
  
  # ########################################
  #  Spatial event distribution through map plotting >> ONLY country and region (ADM1) level
  #     we handle it in the same scale for all the platforms, for comparability purposes
  #   REMARK: It takes time. Moreover, it requires a large amount of space >> need to improve it
  # ########################################
  events_filepath_dict = {}
  events_filepath_dict[consts.NEWS_SURVEILLANCE_PADIWEB] = events_filepath_padiweb
  events_filepath_dict[consts.NEWS_SURVEILLANCE_PROMED] = events_filepath_promed
  events_filepath_dict[consts.NEWS_DB_EMPRESS_I] = events_filepath_empresi
  
  
  out_event_distr_platform_folder = os.path.join(OUT_SPATIAL_ANALYSIS_FOLDER, "event_distribution", "<PLATFORM>")
  for by_continent in ["World"]: # ["World", "EU", "NA", "AS"]
    print("plot spatial distribution map for continent:", by_continent)
    perform_spatial_distribution_map(IN_THEMATIC_TAXONOMY_FOLDER, IN_MAP_SHAPEFILE_FOLDER, events_filepath_dict, out_event_distr_platform_folder, by_continent=by_continent)
  
  
  #########################################
  # Spatio-temporal representativeness >> ONLY country and region (ADM1) level
  ######################################### 
  # PREPARATION
  out_folder = os.path.join(OUT_SPATIAL_ANALYSIS_FOLDER, "spatiotemporal_representativeness")
  out_preprocessing_folder = OUT_PREPROCESSING_FOLDER
  platforms = [consts.NEWS_SURVEILLANCE_PADIWEB, consts.NEWS_SURVEILLANCE_PROMED, consts.NEWS_DB_EMPRESS_I]
  spatial_scales = ["country", "region"] # "country", "region"
  temporal_scales = ["month_no"] # "week_no", "month_no"
  process_temporal_geo_coverage_for_all_platforms(IN_EVENTS_FOLDER, IN_THEMATIC_TAXONOMY_FOLDER, out_folder, out_preprocessing_folder, platforms, spatial_scales, temporal_scales)
  
  # PLOT
  input_folder = os.path.join(OUT_SPATIAL_ANALYSIS_FOLDER, "spatiotemporal_representativeness")
  out_folder = os.path.join(OUT_SPATIAL_ANALYSIS_FOLDER, "spatiotemporal_representativeness")
  ref_platform = consts.NEWS_DB_EMPRESS_I
  platforms = [consts.NEWS_SURVEILLANCE_PADIWEB, consts.NEWS_SURVEILLANCE_PROMED] # consts.NEWS_SURVEILLANCE_PADIWEB, consts.NEWS_SURVEILLANCE_PROMED
  spatial_scales = ["country", "region"] # "country", "region"
  temporal_scales = ["month_no"] # "week_no", "month_no"
  plot_temporal_geo_coverage_results_for_all_platforms(input_folder, out_folder, IN_MAP_SHAPEFILE_FOLDER, ref_platform, platforms, spatial_scales, temporal_scales)
  
  # PLOT
  input_folder = os.path.join(OUT_SPATIAL_ANALYSIS_FOLDER, "spatiotemporal_representativeness")
  out_folder = os.path.join(OUT_SPATIAL_ANALYSIS_FOLDER, "spatiotemporal_representativeness")
  ref_platform = consts.NEWS_DB_EMPRESS_I
  platforms = [consts.NEWS_SURVEILLANCE_PADIWEB, consts.NEWS_SURVEILLANCE_PROMED]
  spatial_scales = ["country", "region"] # "country", "region"
  temporal_scales = ["month_no"] # "week_no", "month_no"
  plot_temporal_geo_coverage_result_comparison_for_all_platforms(input_folder, out_folder, IN_MAP_SHAPEFILE_FOLDER, platforms, ref_platform, spatial_scales, temporal_scales)
  
  # Quantitative evaluation
  # - spatiotemporal geo coverage
  input_folder = os.path.join(OUT_SPATIAL_ANALYSIS_FOLDER, "spatiotemporal_representativeness")
  out_folder = os.path.join(OUT_SPATIAL_ANALYSIS_FOLDER, "spatiotemporal_representativeness")
  ref_platform = consts.NEWS_DB_EMPRESS_I
  platforms = [consts.NEWS_SURVEILLANCE_PADIWEB, consts.NEWS_SURVEILLANCE_PROMED]
  spatial_scales = ["country", "region"] # "country", "region"
  temporal_scales = ["month_no"] # "week_no", "month_no"  
  compute_final_temporal_geo_coverage_result_comparison_for_all_platforms(input_folder, out_folder, platforms, ref_platform, spatial_scales, temporal_scales)
  
  
  
  
  
  
  # # #########################################
  # # TEMPORAL ANALYSIS
  # # ######################################### 
  
  ## --- Timeliness
  input_folder = os.path.join(OUT_FOLDER, "event_matching")
  output_folder = os.path.join(OUT_TEMPORAL_ANALYSIS_FOLDER, "timeliness")
  platforms = [consts.NEWS_SURVEILLANCE_PADIWEB, consts.NEWS_SURVEILLANCE_PROMED]
  ref_platform = consts.NEWS_DB_EMPRESS_I
  #####compute_timeliness_for_all_platforms_old(input_folder, output_folder, platforms)
  compute_timeliness_for_all_platforms(input_folder, output_folder, platforms, ref_platform)
  #####plot_timeliness_for_all_platforms_old(input_folder, output_folder, platforms)
  plot_timeliness_for_all_platforms(input_folder, output_folder, platforms, ref_platform)
  
  
  ## -- Temporal event patterns through the evolution of events >> heatmap
  padiweb_clustering_filepath = os.path.join(input_event_folder_padiweb, "event-clustering.txt")
  promed_clustering_filepath = os.path.join(input_event_folder_promed, "event-clustering.txt")
  output_folder = os.path.join(OUT_TEMPORAL_ANALYSIS_FOLDER, "temporal_patterns")
  countries_of_interest = "CHN,VNM,KOR" # these are alpha3 country codes >> it cannot be empty or "-1"
  year_of_interest = "-1" # "-1" means the whole time period >> # year_of_interest = "2020"
  time_interval_col_name = "biweek_no" # "week_no", "month_no"
  plot_event_evolution_for_all_platforms(MAIN_FOLDER, events_filepath_padiweb, events_filepath_promed, events_filepath_empresi, \
                                         padiweb_clustering_filepath, promed_clustering_filepath, \
                                         output_folder, countries_of_interest, year_of_interest, time_interval_col_name)
  
  
  # -- Spatiotemporal motifs
  #  ---- continuous periodic
  #  ----- seasonal periodic
  # -- motif extraction
  in_folder = IN_EVENTS_FOLDER
  out_folder = OUT_ST_PATTERN_FOLDER
  out_preprocessing_folder = OUT_PREPROCESSING_FOLDER
  platforms = [consts.NEWS_SURVEILLANCE_PADIWEB, consts.NEWS_SURVEILLANCE_PROMED, consts.NEWS_DB_EMPRESS_I]
  for platform_name in platforms:
    ## continuous periodic spatiotemporal motifs
    spatial_scales = ["country", "region"] # "country", "region"
    temporal_scales = ["month_no"]
    process_st_motifs.process_continuous_periodic_st_motif_extraction(in_folder, IN_THEMATIC_TAXONOMY_FOLDER, out_folder, platform_name, out_preprocessing_folder, spatial_scales, temporal_scales)
  
    ## seasonal periodic spatiotemporal motifs
    spatial_scales = ["country"] # "region"
    temporal_scales = ["month_no"] # "week_no", "month_no", "season_no"
    process_st_motifs.process_seasonal_periodic_st_motif_extraction(in_folder, IN_THEMATIC_TAXONOMY_FOLDER, out_folder, platform_name, out_preprocessing_folder, spatial_scales, temporal_scales)
  
  
  # Quantitative evaluation
  # - RANKING
  ref_platform = consts.NEWS_DB_EMPRESS_I
  platforms = [consts.NEWS_SURVEILLANCE_PADIWEB, consts.NEWS_SURVEILLANCE_PROMED]
  in_folder = OUT_ST_PATTERN_FOLDER
  out_folder = OUT_ST_PATTERN_FOLDER
  spatial_scales = ["country", "region"] # "region"
  temporal_scales = ["month_no"] # "week_no", "month_no"
  compute_Kishida_normalized_precision_and_recall_for_continuous_periodic_st_motifs(in_folder, out_folder, ref_platform, platforms, spatial_scales, temporal_scales)
  
  spatial_scales = ["country"] # "region"
  temporal_scales = ["month_no"] # "week_no", "month_no"
  compute_temporal_geo_coverage_for_st_seasonal_periodic_motifs(in_folder, out_folder, ref_platform, platforms, spatial_scales, temporal_scales)
  
  
  
  
  
  
  # #########################################
  # # THEMATIC ENTITY ANALYSIS
  # #########################################
  
  ## -- chord diagram >> circos
  ##   In the plots, the spatial entities are at country level.
  ##   Moreover, the thematic entities are at level 2 (e.g. Avian Influenza (AI) and HPAI)
  output_folder = OUT_THEMATIC_ANALYSIS_FOLDER
  countries_of_interest = "TW,IN,CH,VN,KR,JP" # these are alpha3 country codes >> it cannot be empty or "-1"
  year_of_interest = "-1" # "2020" # "-1" means the whole time period
  time_interval_col_name = "week_no" # # "week_no", "month_no"
  plot_chord_diagram_for_all_platforms(MAIN_FOLDER, events_simplified_filepath_padiweb, events_simplified_filepath_promed, events_simplified_filepath_empresi, \
                                         output_folder, countries_of_interest, year_of_interest, time_interval_col_name)
  
  # -- motif extraction
  in_folder = IN_EVENTS_FOLDER
  out_folder = OUT_THEMATIC_ANALYSIS_FOLDER
  out_preprocessing_folder = OUT_PREPROCESSING_FOLDER
  platforms = [consts.NEWS_SURVEILLANCE_PADIWEB, consts.NEWS_SURVEILLANCE_PROMED, consts.NEWS_DB_EMPRESS_I]
  continents = [""] #  "", "NA", "AF", "SA", "EU", "AS"
  periods = [""] # [2019, 2020, 2021, ""]
  seasons = [""] # ["autumn", "summer", "spring", "winter"]
  for platform_name in platforms:
    process_continuous_periodic_multidim_st_motif_extraction(in_folder, IN_THEMATIC_TAXONOMY_FOLDER, out_folder, platform_name, out_preprocessing_folder, continents, periods, seasons)
  
  
  # Quantitative evaluation
  # - RANKING  
  continents = [""] #  "", "NA", "AF", "SA", "EU", "AS"
  periods = [""] # [2019, 2020, 2021, ""]
  seasons = [""] # ["autumn", "summer", "spring", "winter"]
  ref_platform = consts.NEWS_DB_EMPRESS_I
  platforms = [consts.NEWS_SURVEILLANCE_PADIWEB, consts.NEWS_SURVEILLANCE_PROMED]
  in_folder = OUT_THEMATIC_ANALYSIS_FOLDER
  out_folder = OUT_THEMATIC_ANALYSIS_FOLDER
  compute_Kishida_normalized_precision_and_recall_for_multidim_motifs(in_folder, out_folder, ref_platform, platforms, continents, periods, seasons)
  
  
  
  
  
  #########################################
  # SOURCE ANALYSIS
  #########################################
  
  # PADI-web
  out_news_outlet_padiweb_folder = os.path.join(OUT_NEWS_OUTLET_ANALYSIS_FOLDER, consts.NEWS_SURVEILLANCE_PADIWEB)
  try:
    if not os.path.exists(out_news_outlet_padiweb_folder):
      os.makedirs(out_news_outlet_padiweb_folder)
  except OSError as err:
    print(err)
  
  for by_continent in ["AS", "EU", "-1"]: # "-1" for World >> ["EU", "AS", "NA", "AF", "SA", "-1"]
    print("calculate newslet pagerank scores in padiweb for continent:", by_continent)
    perform_news_outlet_pagerank_analysis(IN_THEMATIC_TAXONOMY_FOLDER, event_candidates_filepath_padiweb, \
                   clustering_result_filepath_padiweb, out_news_outlet_padiweb_folder, by_continent=by_continent)
    
    perform_news_outlet_time_detection_analysis(IN_THEMATIC_TAXONOMY_FOLDER, DATA_SOURCE_GEO_COVERAGE_FOLDER, event_candidates_filepath_padiweb, \
                   clustering_result_filepath_padiweb, out_news_outlet_padiweb_folder, by_continent=by_continent)
  
  
  # ProMED
  out_news_outlet_promed_folder = os.path.join(OUT_NEWS_OUTLET_ANALYSIS_FOLDER, consts.NEWS_SURVEILLANCE_PROMED)
  try:
    if not os.path.exists(out_news_outlet_promed_folder):
      os.makedirs(out_news_outlet_promed_folder)
  except OSError as err:
    print(err)
  
  
  
  #for by_continent in ["EU", "AS", "NA", "AF", "SA", "-1"]: # "-1" for World
  for by_continent in ["AS", "EU", "-1"]: # "-1" for World
    print("calculate newslet pagerank scores in promed for continent:", by_continent)
    perform_news_outlet_pagerank_analysis(IN_THEMATIC_TAXONOMY_FOLDER, event_candidates_filepath_promed, \
                   clustering_result_filepath_promed, out_news_outlet_promed_folder, by_continent=by_continent)
    
    perform_news_outlet_time_detection_analysis(IN_THEMATIC_TAXONOMY_FOLDER, DATA_SOURCE_GEO_COVERAGE_FOLDER, event_candidates_filepath_promed, \
                   clustering_result_filepath_promed, out_news_outlet_promed_folder, by_continent=by_continent)
  
  
  # Quantitative evaluation
  # - RANKING
  by_continent_values = ["-1"]
  platforms = [consts.NEWS_SURVEILLANCE_PADIWEB, consts.NEWS_SURVEILLANCE_PROMED]
  compute_Kishida_normalized_precision_and_recall_for_news_outlets(OUT_NEWS_OUTLET_ANALYSIS_FOLDER, OUT_NEWS_OUTLET_ANALYSIS_FOLDER, platforms, by_continent_values)







  ##################################################################################
  ##################################################################################

  
  ####################################################
  # COMBINE ALL QUANTITATIVE RESULTS >> RADAR CHART
  ####################################################

  platforms = [consts.NEWS_SURVEILLANCE_PADIWEB, consts.NEWS_SURVEILLANCE_PROMED]

  eval_filepath_dict = {}
  column_name_dict = {}
  
  for platform_name in platforms:
    eval_filepath_dict[platform_name] = {}
    column_name_dict[platform_name] = {}
    
    eval_filename = "all_temporal_geo_coverage_results_platform="+platform_name+".csv"
    res_eval_filepath = os.path.join(OUT_SPATIAL_ANALYSIS_FOLDER, "spatiotemporal_representativeness", platform_name, eval_filename)
    eval_filepath_dict[platform_name]["spatial"] = res_eval_filepath
    column_name_dict[platform_name]["spatial"] = "temporal_geocoverage"
    
    eval_filename = "timeliness_"+platform_name+".csv"
    res_eval_filepath = os.path.join(OUT_TEMPORAL_ANALYSIS_FOLDER, "timeliness", eval_filename)
    eval_filepath_dict[platform_name]["temporal: timeliness"] = res_eval_filepath
    column_name_dict[platform_name]["temporal: timeliness"] = "timeliness"
     
    eval_filename = "rank_Kishida_normalized_fmeasure_for_continuous_periodic_st_motifs_"+platform_name+".csv"
    res_eval_filepath = os.path.join(OUT_ST_PATTERN_FOLDER, platform_name, eval_filename)
    eval_filepath_dict[platform_name]["temporal: continuous_periodicity"] = res_eval_filepath
    column_name_dict[platform_name]["temporal: continuous_periodicity"] = "fmeasure"
    
    eval_filename = "temporal_geocoverage_for_seasonal_periodic_st_motifs_"+platform_name+".csv"
    res_eval_filepath = os.path.join(OUT_ST_PATTERN_FOLDER, platform_name, eval_filename)
    eval_filepath_dict[platform_name]["temporal: seasonal_periodicity"] = res_eval_filepath
    column_name_dict[platform_name]["temporal: seasonal_periodicity"] = "temporal_geocoverage"
    
    eval_filename = "rank_Kishida_normalized_fmeasure_for_continuous_periodic_st_multidim_motifs_"+platform_name+".csv"
    res_eval_filepath = os.path.join(OUT_THEMATIC_ANALYSIS_FOLDER, platform_name, eval_filename)
    eval_filepath_dict[platform_name]["thematic"] = res_eval_filepath
    column_name_dict[platform_name]["thematic"] = "fmeasure"
    
    eval_filename = "rank_Kishida_normalized_fmeasure_for_news_outlets_"+platform_name+".csv"
    res_eval_filepath = os.path.join(OUT_NEWS_OUTLET_ANALYSIS_FOLDER, platform_name, eval_filename)
    eval_filepath_dict[platform_name]["source"] = res_eval_filepath
    column_name_dict[platform_name]["source"] = "fmeasure"
    
    
  csv_out_filepath = os.path.join(OUT_FOLDER, "all_quantitative_eval_results.csv")
  plot_output_filepath = os.path.join(OUT_FOLDER, "all_quantitative_eval_results_with_radar_chart.png")
  retrieve_and_plot_all_quantitative_results(platforms, eval_filepath_dict, column_name_dict, csv_out_filepath, plot_output_filepath)
  

  