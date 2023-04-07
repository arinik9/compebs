



import consts
import os


# Libraries
import matplotlib.pyplot as plt
import pandas as pd
from math import pi
 
# # Set data
#
# # version 1
# # df = pd.DataFrame({
# #   'group': ['PADI-web','ProMED'],
# #   'spatial': [0.40, 0.30],
# #   'timeliness': [0.18, 0.13],
# #   'periodicity': [0.59, 0.38],
# #   'thematic': [0.64, 0.53],
# #   'source': [0.96, 0.89]
# # })
#
# # version 2
# df = pd.DataFrame({
#   'group': ['PADI-web','ProMED'],
#   'spatial': [0.40, 0.55],
#   'timeliness': [0.18, 0.12],
#   'periodicity': [0.59, 0.63],
#   'thematic': [0.64, 0.63],
#   'source': [0.96, 0.89]
# })
#
# # # version 1 and 2
# # df = pd.DataFrame({
# #   'group': ['PADI-web', 'ProMED', 'ProMED (only news outlets)'],
# #   'spatial': [0.40, 0.55, 0.30],
# #   'timeliness': [0.18, 0.12, 0.13],
# #   'periodicity': [0.59, 0.63, 0.38],
# #   'thematic': [0.64, 0.63, 0.53],
# #   'source': [0.96, 0.89, 0.89]
# # })
#
 
 
 
def plot_radar_chart_from_df(df, output_filepath):
  
  # ------- PART 1: Create background

  # number of variable
  categories=list(df)[1:]
  N = len(categories)
   
  # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
  angles = [n / float(N) * 2 * pi for n in range(N)]
  angles += angles[:1]
   
  # Initialise the spider plot
  ax = plt.subplot(111, polar=True)
   
  # If you want the first axis to be on top:
  ax.set_theta_offset(pi / 2)
  ax.set_theta_direction(-1)
   
  # Draw one axe per variable + add labels
  plt.xticks(angles[:-1], categories)
   
  # Draw ylabels
  ax.set_rlabel_position(0)
  plt.yticks([0.2,0.4,0.6,0.8,1], ["0.2","0.4","0.6","0.8","1"], color="grey", size=7)
  plt.ylim(0,1)
   
  
  # ------- PART 2: Add plots
   
  # Plot each individual = each line of the data
  # I don't make a loop, because plotting more than 3 groups makes the chart unreadable
   
  # Ind1
  fill_colors = ["b", "r", "g"]
  for i in range(df.shape[0]):
    values=df.loc[i].drop('group').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label=df.loc[i,"group"])
    ax.fill(angles, values, fill_colors[i], alpha=0.1)
   
  # # Ind2
  # values=df.loc[1].drop('group').values.flatten().tolist()
  # values += values[:1]
  # ax.plot(angles, values, linewidth=1, linestyle='solid', label=df.loc[1,"group"])
  # ax.fill(angles, values, 'r', alpha=0.1)
  
  
   
  # Add legend
  plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
  
  # Show the graph
  #plt.show()
  
  plt.savefig(output_filepath)
