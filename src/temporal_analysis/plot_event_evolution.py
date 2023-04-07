'''
Created on Dec 5, 2022

@author: nejat
'''


import os
import subprocess

# Rscript complexheatmap_AI.R "/home/nejat/eclipse/tetis/compebs/in/events/padiweb/event_candidates.csv"
#   "/home/nejat/eclipse/tetis/compebs/in/events/promed/event_candidates.csv" 
#   "/home/nejat/eclipse/tetis/compebs/in/events/empres-i/events.csv" 
#   "/home/nejat/eclipse/tetis/compebs/in/events/padiweb/event-clustering.txt" 
#   "/home/nejat/eclipse/tetis/compebs/in/events/promed/event-clustering.txt" 
#   "/home/nejat/eclipse/tetis/compebs/out/heatmap" "CHN,VNM,KOR" "-1" "biweek_no"


def plot_event_evolution_for_all_platforms(main_folder, padiweb_event_filepath, promed_event_filepath,
                                           empresi_event_filepath, padiweb_clustering_filepath,
                                           promed_clustering_filepath, output_folder,
                                           countries_of_interest, year_of_interest="-1",\
                                            time_interval_col_name="biweek_no"):

  
  R_script_filepath = os.path.join(main_folder, "src", "temporal_analysis", "complexheatmap_AI.R")
  
  run_R_program = subprocess.run(["Rscript", R_script_filepath, padiweb_event_filepath, promed_event_filepath, \
                                   empresi_event_filepath, padiweb_clustering_filepath, promed_clustering_filepath, \
                                   output_folder, countries_of_interest, year_of_interest, time_interval_col_name])


