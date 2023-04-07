'''
Created on Dec 5, 2022

@author: nejat
'''



import subprocess
import os

# Rscript complexheatmap_AI.R "/home/nejat/eclipse/tetis/compebs/in/events/padiweb/event_candidates.csv"
#   "/home/nejat/eclipse/tetis/compebs/in/events/promed/event_candidates.csv" 
#   "/home/nejat/eclipse/tetis/compebs/in/events/empres-i/events.csv" 
#   "/home/nejat/eclipse/tetis/compebs/in/events/padiweb/event-clustering.txt" 
#   "/home/nejat/eclipse/tetis/compebs/in/events/promed/event-clustering.txt" 
#   "/home/nejat/eclipse/tetis/compebs/out/heatmap" "CHN,VNM,KOR" "-1" "biweek_no"


def plot_chord_diagram_for_all_platforms(main_folder, padiweb_event_filepath, promed_event_filepath,
                                           empresi_event_filepath, output_folder,
                                           countries_of_interest, year_of_interest="-1",\
                                            time_interval_col_name="week_no"):

  
  R_script_filepath = os.path.join(main_folder, "src", "thematic_analysis", "circos_AI.R")
  
  run_R_program = subprocess.run(["Rscript", R_script_filepath, padiweb_event_filepath, promed_event_filepath, \
                                   empresi_event_filepath, output_folder, countries_of_interest,\
                                    year_of_interest, time_interval_col_name])


