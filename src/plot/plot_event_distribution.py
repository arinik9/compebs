'''
Created on Apr 2, 2022

@author: nejat
'''

import os
#import seaborn as sns
#import pysal as ps
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
from geopandas import GeoDataFrame
from matplotlib.colors import TwoSlopeNorm
from matplotlib.colors import Normalize

import path
from util_event import read_df_events, read_events_from_df
from util_gis import retrieve_country_alpha2_code_from_alpha3_code



# useful source: https://darribas.org/gds15/content/labs/lab_04.html
# TODO: https://geopandas.org/en/stable/docs/user_guide/interactive_mapping.html



# def reduce_polygon_memory(gdf):
#   # to reduce the size of the output pdf file:
#   # source: https://gis.stackexchange.com/questions/321518/rounding-coordinates-to-5-decimals-in-geopandas
#   #simpledec = re.compile(r"\d*\.\d+")
#   #def mround(match):
#   #  return "{:.2f}".format(float(match.group()))
#   #final_imd.geometry = final_imd.geometry.apply(lambda x: loads(re.sub(simpledec, mround, x.wkt)))
#   new_polygons = []
#   for index, row in gdf.iterrows():    
#     geom = row['geometry']
#     p = wkt.loads(wkt.dumps(geom, rounding_precision=2))
#     new_polygons.append(p)
#   gdf['geometry'] = new_polygons
#   return gdf


# def get_spatial_entity_name_from_coordinates(gdf:GeoDataFrame, p:Point, spatial_column_name:str):
#   spatial_entity_row = gdf[gdf["geometry"].map(p.within)]
#   if spatial_entity_row.shape[0]>0:
#       country = spatial_entity_row["COUNTRY"].iloc[0]
#       spatial_entity = spatial_entity_row[spatial_column_name].iloc[0]
#       return spatial_entity, country # to prevent from any ambiguity (two countries can have the same region names) >> ideally, we should work with ids
#   return None, None


# # 'imd' is  at 'spatial_hierarchy_level'
# def perform_event_distribution(imd:GeoDataFrame, geonameId, country_code, nb_events, spatial_hierarchy_level):
#   try:
#     # spatial_hierarcy = "country"
#     # if event_spatial_hierarchy == "country" and spatial_hierarchy_level == "region":
#     #   spatial_hierarcy = "country"
#     # if event_spatial_hierarchy == "region" and spatial_hierarchy_level == "country":
#     #   spatial_hierarcy = "country"
#     # if event_spatial_hierarchy == "region" and spatial_hierarchy_level == "region":
#     #   spatial_hierarcy = "region"
#
#     i = (imd["CNTR_CODE"] == country_code)
#     if spatial_hierarchy_level == "region":
#       i = (imd["ID"] == geonameId)
#
#     nb_match = imd[i].shape[0]
#     prev_value = imd.loc[i, 'event']
#     imd.loc[i, 'event'] = prev_value + nb_events/nb_match
#   except TopologicalError:
#     print("exception")
#     pass
#
#   return imd


def perform_all_event_distributions(events, imd:GeoDataFrame, spatial_hierarchy_level:str):

  for e in events:    
    nb_events = 1
    
    country_code_alpha3 = e.loc.country_code
    country_code = retrieve_country_alpha2_code_from_alpha3_code(country_code_alpha3)
    
    event_spatial_hierarchy = "country"
    if not e.loc.is_country():
      event_spatial_hierarchy = "region"
      
    geonameId = e.loc.hierarchy_data[0] # default: country level
    i = (imd["CNTR_CODE"] == country_code)

    if event_spatial_hierarchy == "region" and spatial_hierarchy_level == "region":
      geonameId = e.loc.hierarchy_data[1]
      i = (imd["ID"] == geonameId)
      nb_match = imd[i].shape[0]
      if nb_match == 0: # in case of bad geocoding result, we might miss the correct region
        # print("!!!! ERROR with", geonameId, e.loc.hierarchy_data)
        # print(e)
        i = (imd["CNTR_CODE"] == country_code)
        
    nb_match = imd[i].shape[0]
    if nb_match>0:
      prev_value = imd.loc[i, 'event']
      imd.loc[i, 'event'] = prev_value + nb_events/nb_match
      

  return imd



# def add_coarser_hierarchy_info(imd_coarser_level:GeoDataFrame, imd_finer_level:GeoDataFrame, new_column_name:str):
#   values = []
#   for index, row in imd_finer_level.iterrows():
#       geometry = row["geometry"]
#       if not isinstance(geometry, Polygon):
#           geometry = list(geometry)[0]
#       xy = geometry.centroid
#       spatial_entity_name, country = get_spatial_entity_name_from_coordinates(imd_coarser_level, xy, new_column_name)
#       values.append(spatial_entity_name)
#   imd_finer_level[new_column_name] = values
#   return imd_finer_level


def estimate_event_distribution(in_taxonomy_folder, map_shape_data, events_filepath, spatial_hierarchy_level, season, year, out_final_shapefilepath):

  imd = map_shape_data[spatial_hierarchy_level]
  imd["event"] = 0.0 # this is the column that we want to update for map plot

  df_events = read_df_events(events_filepath)
  
  if season != "All":
    df_events = df_events[df_events["season"] == season]
  if year != "All":
    df_events = df_events[df_events["year"] == year]
    
  events = read_events_from_df(df_events, in_taxonomy_folder)
      
  
  if not os.path.isfile(out_final_shapefilepath):
    final_imd = perform_all_event_distributions(events, imd, spatial_hierarchy_level)
    print("FINISHED !!")
    print(spatial_hierarchy_level)
    print(out_final_shapefilepath)
    final_imd.to_file(driver = 'ESRI Shapefile', filename = out_final_shapefilepath, encoding = "utf-8")
  else:
    print("output shapefilepath already exists !")



def plot_event_distribution(out_final_shapefilepath, out_map_figure_filepath, limits, \
                                continent_name):
  plot_event_distribution_generic(out_final_shapefilepath, out_map_figure_filepath, limits, \
                                      continent_name, "event", False)



def plot_event_distribution_generic(out_final_shapefilepath, out_map_figure_filepath, limits, \
                                       continent_name, column_name, display_country_code, display_nan_values=False):
  
  # imd_world = gpd.read_file(country_shapefilepath, encoding = "utf-8")
  # imd_world = imd_world.to_crs(4326)
  
  country_code_fontsize = 20
  
  final_imd = None
  if os.path.isfile(out_final_shapefilepath):
    final_imd = gpd.read_file(out_final_shapefilepath, encoding = "utf-8")
    final_imd = final_imd.to_crs(4326)
    final_imd.fillna(value=np.nan, inplace=True)
    final_imd = final_imd.astype({column_name:'float'})
    #final_imd.fillna('', inplace=True)
    #print(final_imd)
    ##topo = tp.Topology(final_imd['geometry'], prequantize=False)
    ##final_imd['geometry'] = topo.toposimplify(1).to_gdf()
      
    #final_imd = reduce_polygon_memory(final_imd)
    #final_imd['geometry'] = final_imd['geometry'].simplify(0.1, True)
    
    country_code = None
    if 'CNTR_CODE' in final_imd.columns:
      country_code = 'CNTR_CODE'
    elif 'ISO_A2' in final_imd.columns:
      country_code = 'ISO_A2'
    elif 'iso_a2' in final_imd.columns:
      country_code = 'iso_a2'
    elif 'isocode' in final_imd.columns:
      country_code = 'isocode'
    
    
    # preprocessing >> imd_world can be at country or ADM1 level
    imd_country = final_imd.dissolve(by=country_code).reset_index()
    
    norm = Normalize(vmin=0.05, vmax=max(limits))

    # https://matplotlib.org/2.0.2/users/colormaps.html
    width = 4.8*4 # default, for europe map
    height = 6.4*3 # default, for europe map
    if continent_name == "AS":
      width = 4.25*4 # default, for europe map
      height = 6*2
      country_code_fontsize = 20
    elif continent_name == "NA":
      width = 4.5*3 # default, for europe map
      height = 6*2
      country_code_fontsize = 20
    elif continent_name == "world":
      width = 4.5*3 # default, for world map
      height = 6
      country_code_fontsize = 6
    fig, ax = plt.subplots(figsize=(width, height), tight_layout = True)
    final_imd_event_zero = final_imd[final_imd[column_name] < 0.00001]
    final_imd_event_non_zero = final_imd[final_imd[column_name] > 0.00001]
    ax = final_imd_event_non_zero.plot(ax=ax, column=column_name, colormap=plt.cm.Blues, norm=norm, legend=True, linewidth=0, legend_kwds={'fraction':0.03, 'pad':0.04})
    #final_imd_event_non_hotspot = final_imd_event_non_zero[final_imd_event_non_zero["event"] <= 2]
    #final_imd_event_hotspot = final_imd_event_non_zero[final_imd_event_non_zero["event"] > 2]
    #plt.rc('legend',fontsize=20) # using a size in points
    #ax = final_imd_event_non_hotspot.plot(ax=ax, column='event', scheme="User_Defined", classification_kwds=dict(bins=bins), colormap=plt.cm.Blues, legend=True)
    #plt.rcParams['hatch.color'] = "orange"
    #ax = final_imd_event_hotspot.plot(ax=ax, column='event', scheme="User_Defined", classification_kwds=dict(bins=bins), colormap=plt.cm.Blues, hatch="//", legend=False)
    #ax = final_imd_event_hotspot.plot(ax=ax, column='event', scheme="User_Defined", classification_kwds=dict(bins=bins), colormap=plt.cm.Blues, legend=False)
    ax = final_imd_event_zero.plot(ax=ax, column=column_name, color="white", linewidth=0, legend=False) # we exclude this part from the discretization of the colors
    if display_nan_values:
      final_imd_event_null = final_imd[final_imd[column_name].isnull()]
      ax = final_imd_event_null.plot(ax=ax, column=column_name, color="lightgrey", linewidth=0, legend=False)
    _ = ax.axis('off')
    # highlight the US region borders in red
    final_imd.plot(ax=ax, facecolor='none', linewidth=0.3, edgecolor='grey')
    imd_country.plot(ax=ax, facecolor='none', linewidth=0.3, edgecolor='black')
    
    
    # add/annotate region names at the centroid point of the US regions
    if display_country_code:
      for idx, row in imd_country.iterrows():
        geometry = row['geometry']
        if not isinstance(geometry, Polygon):
          geometry = max(geometry, key=lambda a: a.area)
        country_code_value = row[country_code]
        if country_code_value != '-1':
          plt.annotate(text=country_code_value, xy=geometry.centroid.coords[0], horizontalalignment='center', color="orange", fontsize=country_code_fontsize)
    #plt.show()
    fig.savefig(out_map_figure_filepath, bbox_inches = 'tight')
  else:
    print("output shapefile does not exist !")
    
    
    
# def plot_map_for_categorical_variable_generic(out_final_shapefilepath, out_map_figure_filepath, \
#                                        continent_name, column_name, display_country_code, display_nan_values=False):
#   COLORS = ['orange', 'darkviolet', 'deeppink', 'olivedrab', 'dodgerblue', 'gold', 'goldenroad',  'cyan']
#
#   # imd_world = gpd.read_file(country_shapefilepath, encoding = "utf-8")
#   # imd_world = imd_world.to_crs(4326)
#
#   country_code_fontsize = 20
#
#   final_imd = None
#   if os.path.isfile(out_final_shapefilepath):
#     final_imd = gpd.read_file(out_final_shapefilepath, encoding = "utf-8")
#     final_imd = final_imd.to_crs(4326)
#     final_imd.fillna(value=np.nan, inplace=True)
#     final_imd = final_imd.astype({column_name:'float'})
#
#     country_code = None
#     if 'CNTR_CODE' in imd_world.columns:
#       country_code = 'CNTR_CODE'
#     elif 'ISO_A2' in imd_world.columns:
#       country_code = 'ISO_A2'
#     elif 'iso_a2' in imd_world.columns:
#       country_code = 'iso_a2'
#     elif 'isocode' in imd_world.columns:
#       country_code = 'isocode'
#
#     # preprocessing >> imd_world can be at country or ADM1 level
#     imd_country = imd_world.dissolve(by=country_code).reset_index()
#
#     cat_var_values = np.unique(final_imd[column_name].to_list())
#
#     #final_imd.fillna('', inplace=True)
#     #print(final_imd)
#     ##topo = tp.Topology(final_imd['geometry'], prequantize=False)
#     ##final_imd['geometry'] = topo.toposimplify(1).to_gdf()
#
#     final_imd = reduce_polygon_memory(final_imd)
#     #final_imd['geometry'] = final_imd['geometry'].simplify(0.1, True)
#
#
#     # https://matplotlib.org/2.0.2/users/colormaps.html
#     width = 4.8*4 # default, for europe map
#     height = 6.4*3 # default, for europe map
#     if continent_name == "AS":
#       width = 4.25*4 # default, for europe map
#       height = 6*2
#       country_code_fontsize = 20
#     elif continent_name == "NA":
#       width = 4.5*3 # default, for europe map
#       height = 6*2
#       country_code_fontsize = 20
#     elif continent_name == "world":
#       width = 4.5*3 # default, for world map
#       height = 6
#       country_code_fontsize = 6
#
#     fig, ax = plt.subplots(figsize=(width, height), tight_layout = True)
#     for i in range(len(cat_var_values)):
#       print("--", i)
#       print(COLORS[i])
#       cat_var_val = cat_var_values[i]
#       curr_imd = final_imd[final_imd[column_name] == cat_var_val]
#       ax = curr_imd.plot(ax=ax, column=column_name, color=COLORS[i], legend=True, linewidth=0, legend_kwds={'fraction':0.03, 'pad':0.04})
#
#     #final_imd_event_non_hotspot = final_imd_event_non_zero[final_imd_event_non_zero["event"] <= 2]
#     #final_imd_event_hotspot = final_imd_event_non_zero[final_imd_event_non_zero["event"] > 2]
#     #plt.rc('legend',fontsize=20) # using a size in points
#     #ax = final_imd_event_non_hotspot.plot(ax=ax, column='event', scheme="User_Defined", classification_kwds=dict(bins=bins), colormap=plt.cm.Blues, legend=True)
#     #plt.rcParams['hatch.color'] = "orange"
#     #ax = final_imd_event_hotspot.plot(ax=ax, column='event', scheme="User_Defined", classification_kwds=dict(bins=bins), colormap=plt.cm.Blues, hatch="//", legend=False)
#     #ax = final_imd_event_hotspot.plot(ax=ax, column='event', scheme="User_Defined", classification_kwds=dict(bins=bins), colormap=plt.cm.Blues, legend=False)
#     if display_nan_values:
#       final_imd_event_null = final_imd[final_imd[column_name].isnull()]
#       ax = final_imd_event_null.plot(ax=ax, column=column_name, color="lightgrey", linewidth=0, legend=False)
#     _ = ax.axis('off')
#     # highlight the US region borders in red
#     final_imd.plot(ax=ax, facecolor='none', linewidth=0.3, edgecolor='grey')
#     imd_country.plot(ax=ax, facecolor='none', linewidth=0.3, edgecolor='black')
#
#     # add/annotate region names at the centroid point of the US regions
#     if display_country_code:
#       for idx, row in imd_country.iterrows():
#         geometry = row['geometry']
#         if not isinstance(geometry, Polygon):
#           geometry = max(geometry, key=lambda a: a.area)
#         country_code_value = row[country_code]
#         if country_code_value != '-1':
#           plt.annotate(text=country_code_value, xy=geometry.centroid.coords[0], horizontalalignment='center', color="black", fontsize=country_code_fontsize)
#     #plt.show()
#     fig.savefig(out_map_figure_filepath, bbox_inches = 'tight')
#   else:
#     print("output shapefile does not exist !")



def comparison_plot_map(padiweb_event_distr_shapefilepath, healthmap_event_distr_shapefilepath, \
                        comparison_map_figure_filepath, limits, continent_name, column_name="event",\
                         display_country_code=False, display_nan_values=False):
  gdf_padiweb = gpd.read_file(padiweb_event_distr_shapefilepath, encoding = "utf-8")
  gdf_padiweb = gdf_padiweb.to_crs(4326)
  gdf_padiweb.fillna(value=np.nan, inplace=True)
  gdf_padiweb = gdf_padiweb.astype({column_name:'float'})
  # Do not set to 0 since 0 is a valid observation in terms of spatial analysis
  padiweb_nb_events = gdf_padiweb[column_name].to_numpy() 

  gdf_healthmap = gpd.read_file(healthmap_event_distr_shapefilepath, encoding = "utf-8")
  gdf_healthmap = gdf_healthmap.to_crs(4326)
  gdf_healthmap.fillna(value=np.nan, inplace=True)
  gdf_healthmap = gdf_healthmap.astype({column_name:'float'})
  # Do not set to 0 since 0 is a valid observation in terms of spatial analysis
  healthmap_nb_events = gdf_healthmap[column_name].to_numpy()
  
  print("display_country_code:", display_country_code)
  
  # --------------------------------------------------------
  # we plot the comparison based on the padiweb geodataframe
  #gdf_padiweb = reduce_polygon_memory(gdf_padiweb)
  #gdf_padiweb['geometry'] = gdf_padiweb['geometry'].simplify(0.1, True)
  
  gdf_padiweb['difference'] = (padiweb_nb_events-healthmap_nb_events) # element-wise difference
  diff_values = gdf_padiweb['difference'].to_numpy()
  #padiweb_greater = gdf_padiweb.loc[(diff_values>0), ['difference', 'geometry']]
  #healthmap_greater = gdf_padiweb.loc[(diff_values<0), ['difference', 'geometry']]
  padiweb_healthmap_equal_non_zero = gdf_padiweb.loc[(diff_values == 0) & (padiweb_nb_events != 0), ['difference', 'geometry']]
  #padiweb_healthmap_equal_zero = gdf_padiweb.loc[(diff_values == 0) & (padiweb_nb_events == 0), ['difference', 'geometry']]

  country_code_fontsize = 20
  
  column_country_code = None
  if 'CNTR_CODE' in gdf_padiweb.columns:
    column_country_code = 'CNTR_CODE'
  elif 'ISO_A2' in gdf_padiweb.columns:
    column_country_code = 'ISO_A2'
  elif 'iso_a2' in gdf_padiweb.columns:
    column_country_code = 'iso_a2'
  elif 'isocode' in gdf_padiweb.columns:
    column_country_code = 'isocode'
    
  # preprocessing >> imd_world can be at country or ADM1 level
  imd_country = gdf_padiweb.dissolve(by=column_country_code).reset_index()
  
  # plot
  # https://gis.stackexchange.com/questions/330008/center-normalize-choropleth-colors-in-geopandas
  # https://stackoverflow.com/questions/25500541/matplotlib-bwr-colormap-always-centered-on-zero
  width = 4.8*4 # default, for europe map
  height = 6.4*3 # default, for europe map
  if continent_name == "AS":
    width = 4.25*4 # default, for europe map
    height = 6*2
    country_code_fontsize = 20
  elif continent_name == "NA":
    width = 4.5*3 # default, for europe map
    height = 6*2
    country_code_fontsize = 20
  elif continent_name == "world":
    width = 4.5*3 # default, for world map
    height = 6
    country_code_fontsize = 6
  fig, ax = plt.subplots(figsize=(width, height), tight_layout = True)
  ec = '0.8'
  # plot significant data
  #bins = mapclassify.EqualInterval(gdf_padiweb['difference'], k=8).bins
  vmin=min(limits)
  if vmin == 0:
    vmin = -0.1
  norm = TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=max(limits))
  gdf_padiweb.plot(ax=ax, edgecolor=ec, linewidth=0.1, column='difference', colormap=plt.cm.bwr, norm=norm, legend=True, legend_kwds={'fraction':0.03, 'pad':0.04})
  padiweb_healthmap_equal_non_zero.plot(ax=ax, column='difference', color='wheat', edgecolor=ec, linewidth=0.1)
  #padiweb_healthmap_equal_zero.plot(ax=ax, column='difference', color='white', edgecolor=ec, linewidth=0.1)

  #handles, labels = ax.get_legend_handles_labels()
  #ax.legend(handles, labels)
  if display_nan_values:
    final_imd_event_null = gdf_padiweb.loc[np.isnan(diff_values), ['difference', 'geometry']]
    ax = final_imd_event_null.plot(ax=ax, column=column_name, color="lightgrey", linewidth=0, legend=False)


  # imd_country = gpd.read_file(country_shapefilepath, encoding = "utf-8")
  # imd_country = imd_country.to_crs(4326)
  
  gdf_padiweb.plot(ax=ax, facecolor='none', linewidth=0.3, edgecolor='grey')
  imd_country.plot(ax=ax, facecolor='none', linewidth=0.3, edgecolor='black')
  _ = ax.axis('off')

  # add/annotate region names at the centroid point of the US regions
  if display_country_code:
    for idx, row in imd_country.iterrows():
      geometry = row['geometry']
      if not isinstance(geometry, Polygon):
        geometry = max(geometry, key=lambda a: a.area)
      country_code_value = row[column_country_code]
      if country_code_value != '-1':
        plt.annotate(text=country_code_value, xy=geometry.centroid.coords[0], horizontalalignment='center', color="orange", fontsize=country_code_fontsize)

  # https://matplotlib.org/3.5.1/tutorials/intermediate/legend_guide.html#creating-artists-specifically-for-adding-to-the-legend-aka-proxy-artists
  #patches = []
  #patches.append(mpatches.Patch(color='lightgrey', label='event(PADI-Web) = event(PROMED)'))
  #ax.legend(handles=patches)

  ax.set_axis_off()
  fig.savefig(comparison_map_figure_filepath)  
    
 
 
 


# ===============================================================================================================


def prepare_asia_shape_data(input_shapefile_folder):
  output = {}

  county_shapefilepath = os.path.join(input_shapefile_folder, "asia", "asia_ne10_admin_level2.shp")
  imd_county = gpd.read_file(county_shapefilepath, encoding = "utf-8")
  imd_county = imd_county.to_crs(4326)
  imd_county = imd_county.rename(index=str, columns={"name_2":"CITY"})
  imd_county = imd_county.rename(index=str, columns={"name_1":"REGION"})
  imd_county = imd_county.rename(index=str, columns={"name_0":"COUNTRY"})

  state_shapefilepath = os.path.join(input_shapefile_folder, "asia", "asia_ne10_admin_level1.shp")
  imd_state = gpd.read_file(state_shapefilepath, encoding = "utf-8")
  imd_state = imd_state.to_crs(4326)
  imd_state = imd_state.rename(index=str, columns={"name_1":"REGION"})
  imd_state = imd_state.rename(index=str, columns={"name_0":"COUNTRY"})

  country_shapefilepath = os.path.join(input_shapefile_folder, "asia", "asia_ne10_admin_level0.shp")
  imd_country = gpd.read_file(country_shapefilepath, encoding = "utf-8")
  imd_country = imd_country.to_crs(4326)
  imd_country = imd_country.rename(index=str, columns={"name_engli":"COUNTRY"})
  imd_country = imd_country.rename(index=str, columns={"iso":"CNTR_CODE"})

  output["region"] = imd_state
  output["city"] = imd_county
  output["country"] = imd_country

  return output



# It takes in input a shapefile path at city level, and returns three geodataframe: country shape, region shape and city shape data
def prepare_US_shape_data(input_shapefile_folder):
  output = {}

  county_shapefilepath = os.path.join(input_shapefile_folder, "us", "cb_2020_us_county_5m", "cb_2020_us_county_5m.shp")
  state_shapefilepath = os.path.join(input_shapefile_folder, "us", "cb_2020_us_state_5m", "cb_2020_us_state_5m.shp")

  imd_county = gpd.read_file(county_shapefilepath, encoding = "utf-8")
  imd_county = imd_county.to_crs(4326)
  imd_county["COUNTRY"] = "United States"
  imd_county = imd_county.rename(index=str, columns={"NAME":"CITY"})
  imd_county = imd_county.rename(index=str, columns={"STATE_NAME":"REGION"})


  imd_state = gpd.read_file(state_shapefilepath, encoding = "utf-8")
  imd_state = imd_state.to_crs(4326)
  imd_state["COUNTRY"] = "United States"
  imd_state = imd_state.rename(index=str, columns={"NAME":"REGION"})
  imd_state = imd_state.rename(index=str, columns={"STUSPS":"CNTR_CODE"})

  output["region"] = imd_state
  output["city"] = imd_county

  return output



def prepare_world_shape_data(input_shapefile_folder):
  output = {}
  
  state_shapefilepath = os.path.join(input_shapefile_folder, "world", "ne_10m_admin_1_states_provinces", "naturalearth_adm1.shp")
  imd_state = gpd.read_file(state_shapefilepath, encoding = "utf8")
  imd_state = imd_state.to_crs(4326)
  imd_state = imd_state.rename(index=str, columns={"name":"REGION", "admin":"COUNTRY", "iso_a2":"CNTR_CODE", "gn_id":"ID"})
  imd_state = imd_state.astype({"ID":'int'})
  
  country_shapefilepath = os.path.join(input_shapefile_folder, "world", "gaul0_asap", "gaul0_asap.shp")
  imd_country = gpd.read_file(country_shapefilepath, encoding = "utf8")
  imd_country = imd_country.to_crs(4326)
  imd_country = imd_country.rename(index=str, columns={"name0":"COUNTRY", "isocode":"CNTR_CODE", "gn_id":"ID"})
  
  output["region"] = imd_state
  output["country"] = imd_country
  return output
  


def prepare_north_america_shape_data(input_shapefile_folder):
  output = {}

  county_shapefilepath = os.path.join(input_shapefile_folder, "americas", "north_america_ne10_admin_level2.shp")
  imd_county = gpd.read_file(county_shapefilepath, encoding = "iso8859-1")
  imd_county = imd_county.to_crs(4326)
  imd_county = imd_county.rename(index=str, columns={"name_2":"CITY"})
  imd_county = imd_county.rename(index=str, columns={"name_1":"REGION"})
  imd_county = imd_county.rename(index=str, columns={"name_0":"COUNTRY"})

  state_shapefilepath = os.path.join(input_shapefile_folder, "americas", "north_america_ne10_admin_level1.shp")
  imd_state = gpd.read_file(state_shapefilepath, encoding = "iso8859-1")
  imd_state = imd_state.to_crs(4326)
  imd_state = imd_state.rename(index=str, columns={"name_1":"REGION"})
  imd_state = imd_state.rename(index=str, columns={"name_0":"COUNTRY"})

  country_shapefilepath = os.path.join(input_shapefile_folder, "americas", "north_america_ne10_admin_level0.shp")
  imd_country = gpd.read_file(country_shapefilepath, encoding = "iso8859-1")
  imd_country = imd_country.to_crs(4326)
  imd_country = imd_country.rename(index=str, columns={"name_engli":"COUNTRY"})
  imd_country = imd_country.rename(index=str, columns={"iso":"CNTR_CODE"})
  #imd_country = gpd.clip(imd_country, imd_state)
  #print("clip finished !!")
  #imd_country.to_file(driver = 'ESRI Shapefile', filename = "/home/nejat/usa_national_border.shp", encoding = "utf-8")

  output["region"] = imd_state
  output["city"] = imd_county
  output["country"] = imd_country

  return output



def get_spatial_entity_name_from_coordinates(gdf:GeoDataFrame, p:Point, spatial_column_name:str):
  spatial_entity_row = gdf[gdf["geometry"].map(p.within)]
  if spatial_entity_row.shape[0]>0:
      country = spatial_entity_row["COUNTRY"].iloc[0]
      spatial_entity = spatial_entity_row[spatial_column_name].iloc[0]
      return spatial_entity, country # to prevent from any ambiguity (two countries can have the same region names) >> ideally, we should work with ids
  return None, None

def add_coarser_hierarchy_info(imd_coarser_level:GeoDataFrame, imd_finer_level:GeoDataFrame, new_column_name:str):
  values = []
  for index, row in imd_finer_level.iterrows():
      geometry = row["geometry"]
      if not isinstance(geometry, Polygon):
          geometry = list(geometry)[0]
      xy = geometry.centroid
      spatial_entity_name, country = get_spatial_entity_name_from_coordinates(imd_coarser_level, xy, new_column_name)
      values.append(spatial_entity_name)
  imd_finer_level[new_column_name] = values
  return imd_finer_level


# It takes in input a shapefile path at city level, and returns three geodataframe: country shape, region shape and city shape data
def prepare_europe_shape_data(input_shapefile_folder):
  output = {}

  # at country level
  country_shapefilepath = os.path.join(input_shapefile_folder, "europe", "NUTS_RG_10M_2021_4326_country_level.shp")
  imd_country = gpd.read_file(country_shapefilepath, encoding = "utf-8")
  imd_country = imd_country.to_crs(4326)
  imd_country = imd_country.rename(index=str, columns={"NAME_LATN":"COUNTRY"})
  imd_country['geometry'] = imd_country.buffer(0)

  # at region level  
  region_shapefilepath = os.path.join(input_shapefile_folder, "europe", "NUTS_RG_10M_2021_4326_region_level.shp")
  imd_region = gpd.read_file(region_shapefilepath, encoding = "utf-8")
  imd_region = imd_region.to_crs(4326)
  imd_region = imd_region.rename(index=str, columns={"NAME_LATN":"REGION"})
  imd_region = add_coarser_hierarchy_info(imd_country, imd_region, "COUNTRY")
  imd_region['geometry'] = imd_region.buffer(0)

  # at city level  
  city_shapefilepath = os.path.join(input_shapefile_folder, "europe", "NUTS_RG_10M_2021_4326_city_level.shp")
  imd_city = gpd.read_file(city_shapefilepath, encoding = "utf-8")
  imd_city = imd_city.to_crs(4326)
  imd_city = imd_city.rename(index=str, columns={"NAME_LATN":"CITY"})
  imd_city = add_coarser_hierarchy_info(imd_country, imd_city, "COUNTRY")
  imd_city = add_coarser_hierarchy_info(imd_region, imd_city, "REGION")  
  imd_city['geometry'] = imd_city.buffer(0)

  output["country"] = imd_country
  output["region"] = imd_region
  output["city"] = imd_city

  return output


# ===============================================================================================================


def prepare_EU_map_data(in_taxonomy_folder, input_shapefile_folder, events_filepath, out_final_shapefilepath, spatial_hierarchy_level, season, year):
  print("prepare EU map data")
  map_shape_data = prepare_europe_shape_data(input_shapefile_folder)
  # -----------------------------------------------------
  # bug to handle:
  # res = get_spatial_entity_name_from_coordinates(map_shape_data["city"], Point(-3.40233, 50.61723), "COUNTRY")
  # -----------------------------------------------------
  estimate_event_distribution(in_taxonomy_folder, map_shape_data, events_filepath, spatial_hierarchy_level, season, year, out_final_shapefilepath)





def prepare_world_map_data(in_taxonomy_folder, input_shapefile_folder, events_filepath, out_final_shapefilepath, spatial_hierarchy_level, season, year):
  print("prepare WORLD map data")
  map_shape_data = prepare_world_shape_data(input_shapefile_folder)
  estimate_event_distribution(in_taxonomy_folder, map_shape_data, events_filepath, spatial_hierarchy_level, season, year, out_final_shapefilepath)



def prepare_US_map_data(in_taxonomy_folder, input_shapefile_folder, events_filepath, out_final_shapefilepath, spatial_hierarchy_level, season, year):
  print("prepare US map data")
  map_shape_data = prepare_US_shape_data(input_shapefile_folder)
  estimate_event_distribution(in_taxonomy_folder, map_shape_data, events_filepath, spatial_hierarchy_level, season, year, out_final_shapefilepath)



def prepare_north_america_map_data(in_taxonomy_folder, input_shapefile_folder, events_filepath, out_final_shapefilepath, spatial_hierarchy_level, season, year):
  print("prepare NORTH AMERICA map data")
  map_shape_data = prepare_north_america_shape_data(input_shapefile_folder)
  estimate_event_distribution(in_taxonomy_folder, map_shape_data, events_filepath, spatial_hierarchy_level, season, year, out_final_shapefilepath)



def prepare_asia_map_data(in_taxonomy_folder, input_shapefile_folder, events_filepath, out_final_shapefilepath, spatial_hierarchy_level, season, year):
  print("prepare ASIA map data")
  map_shape_data = prepare_asia_shape_data(input_shapefile_folder)
  estimate_event_distribution(in_taxonomy_folder, map_shape_data, events_filepath, spatial_hierarchy_level, season, year, out_final_shapefilepath)




# ===============================================================================================================

# def determine_bins(event_dist_filepath_list):
#   event_values = []
#
#   for filepath in event_dist_filepath_list:
#     imd = gpd.read_file(filepath, encoding = "utf-8")
#     imd = imd.to_crs(4326)
#     imd = imd[imd['event'] != 0.0]
#     event_values.extend(imd["event"].to_list())
#
#   # prepare common bins for coloring
#   bins = mapclassify.Quantiles(event_values, k=6).bins
#   return bins
  

def determine_plot_limits(event_distr_shapefilepath_list):
  limit_values = []
  for filepath in event_distr_shapefilepath_list:
    imd = gpd.read_file(filepath, encoding = "utf-8")
    imd = imd.to_crs(4326)
    imd = imd[imd['event'] != 0.0]
    non_zero_vals = imd["event"].to_list()
    if len(non_zero_vals)>0:
      min_max = [min(non_zero_vals), max(non_zero_vals)]
      limit_values.extend(min_max)

  limits = (min(limit_values), max(limit_values))
  return limits



def determine_comparison_plot_limits(platform1_event_distr_shapefilepath_list, platform2_event_distr_shapefilepath_list):
  limit_values = []
  nb_platforms = len(platform1_event_distr_shapefilepath_list)
  for i in range(nb_platforms):
    filepath1 = platform1_event_distr_shapefilepath_list[i]
    filepath2 = platform2_event_distr_shapefilepath_list[i]
    
    imd_platform1 = gpd.read_file(filepath1, encoding = "utf-8")
    imd_platform1 = imd_platform1.to_crs(4326)
    imd_platform2 = gpd.read_file(filepath2, encoding = "utf-8")
    imd_platform2 = imd_platform2.to_crs(4326)
    
    diff_values = imd_platform1["event"].to_numpy() -imd_platform2["event"].to_numpy()
    if len(diff_values)>0:
      min_max = [min(diff_values), max(diff_values)]
      limit_values.extend(min_max)

  limits = (min(limit_values), max(limit_values))
  return limits





def prepare_all_event_distributions(in_taxonomy_folder, input_shapefile_folder, events_filepath_dict, output_dirpath, continent_name, seasons, periods, spatial_hierarchy_levels):

  for platform in events_filepath_dict.keys():
    events_filepath = events_filepath_dict[platform]

    for season in seasons:
      for year in periods:
        input_folder = path.get_event_distribution_folder_path(output_dirpath, platform, continent_name, season, year)
        print(output_dirpath)
        print(input_folder)
        try:
          if not os.path.exists(input_folder):
            os.makedirs(input_folder)
        except OSError as err:
          print(err)

        print("------------------ prepare " + platform + " ---------------------")
        for spatial_hierarchy_level in spatial_hierarchy_levels:
          print("prepare at " + spatial_hierarchy_level + " level ..")
          event_distr_shapefilepath = os.path.join(input_folder, platform + "_event_distr_at_"+spatial_hierarchy_level+"_level.shp")

          if continent_name == "World":
            prepare_world_map_data(in_taxonomy_folder, input_shapefile_folder, events_filepath, event_distr_shapefilepath, spatial_hierarchy_level, season, year)
          elif continent_name == "NA":
            prepare_north_america_map_data(in_taxonomy_folder, input_shapefile_folder, events_filepath, event_distr_shapefilepath, spatial_hierarchy_level, season, year)
          elif continent_name == "EU":
            prepare_EU_map_data(in_taxonomy_folder, input_shapefile_folder, events_filepath, event_distr_shapefilepath, spatial_hierarchy_level, season, year)
          elif continent_name == "AS":
            prepare_asia_map_data(in_taxonomy_folder, input_shapefile_folder, events_filepath, event_distr_shapefilepath, spatial_hierarchy_level, season, year)




def plot_all_event_distributions(platforms, output_dirpath, continent_name, seasons, periods, spatial_hierarchy_levels):
  
  print("------------------ prepare plot limits ---------------------")
  event_distr_shapefilepath_list = []
  for platform in platforms:
    for spatial_hierarchy_level in spatial_hierarchy_levels:
      for season in seasons:
        for year in periods:      
          input_folder = path.get_event_distribution_folder_path(output_dirpath, platform, continent_name, season, year)
          event_distr_shapefilepath = os.path.join(input_folder, platform + "_event_distr_at_"+spatial_hierarchy_level+"_level.shp")
          event_distr_shapefilepath_list.append(event_distr_shapefilepath)

  limits = determine_plot_limits(event_distr_shapefilepath_list)
  print(limits)
  # --------------------------------------------------------------------------------------------------------------------------
  
  for platform in platforms:
    for season in seasons:
      for year in periods:    
        input_folder = path.get_event_distribution_folder_path(output_dirpath, platform, continent_name, season, year)
             
        # padiweb
        print("------------------ plot " + platform + " ---------------------")
        for spatial_hierarchy_level in spatial_hierarchy_levels:
          print("plot PADIWEB at " + spatial_hierarchy_level + " level ..")
          #country_shapefilepath = os.path.join(input_folder, platform + "_event_distr_at_"+spatial_hierarchy_level+"_level.shp")
          event_distr_shapefilepath = os.path.join(input_folder, platform + "_event_distr_at_"+spatial_hierarchy_level+"_level.shp")
          #map_figure_filepath = os.path.join(input_folder,  platform + "_event_distr_at_"+spatial_hierarchy_level+"_level.pdf")
          map_figure_filepath = os.path.join(input_folder,  platform + "_event_distr_at_"+spatial_hierarchy_level+"_level.png")
          plot_event_distribution(event_distr_shapefilepath, map_figure_filepath, limits, continent_name)
      
      

def plot_all_event_comparison_maps(platforms, output_dirpath, continent_name, seasons, periods, spatial_hierarchy_levels):

  if len(platforms)<2:
    print("There should be at least 2 platforms for the comparison ...")
    return 

  print("------------------ prepare plot limits ---------------------")
  platform1_event_distr_shapefilepath_list = []
  platform2_event_distr_shapefilepath_list = []
  for i in range(0,len(platforms)):
    platform1 = platforms[i]
    for j in range(i+1,len(platforms)):
      platform2 = platforms[j]
      
      for spatial_hierarchy_level in spatial_hierarchy_levels:
        for season in seasons:
          for year in periods:      
            platform1_input_folder = path.get_event_distribution_folder_path(output_dirpath, platform1, continent_name, season, year)
            platform1_event_distr_shapefilepath = os.path.join(platform1_input_folder, platform1 + "_event_distr_at_"+spatial_hierarchy_level+"_level.shp")
            platform1_event_distr_shapefilepath_list.append(platform1_event_distr_shapefilepath)
            #
            platform2_input_folder = path.get_event_distribution_folder_path(output_dirpath, platform2, continent_name, season, year)
            platform2_event_distr_shapefilepath = os.path.join(platform2_input_folder, platform2 + "_event_distr_at_"+spatial_hierarchy_level+"_level.shp")
            platform2_event_distr_shapefilepath_list.append(platform2_event_distr_shapefilepath)
      
  limits = determine_comparison_plot_limits(platform1_event_distr_shapefilepath_list, platform2_event_distr_shapefilepath_list)
  print(limits)
  # --------------------------------------------------------------------------------------------------------------------------



  print("------------------ compare event distribution ---------------------")
  for i in range(0,len(platforms)):
    platform1 = platforms[i]
    for j in range(i+1,len(platforms)):
      platform2 = platforms[j]
      
      for season in seasons:
        for year in periods:    
          output_folder = path.get_event_distribution_folder_path(output_dirpath, platform1+"_"+platform2, continent_name, season, year)
          platform1_input_folder = path.get_event_distribution_folder_path(output_dirpath, platform1, continent_name, season, year)
          platform2_input_folder = path.get_event_distribution_folder_path(output_dirpath, platform2, continent_name, season, year) 
               
          try:
            if not os.path.exists(output_folder):
              os.makedirs(output_folder)
          except OSError as err:
             print(err)
                    
          for spatial_hierarchy_level in spatial_hierarchy_levels:
            print("compare event distribution at " + spatial_hierarchy_level + " level ..")
            
            #country_shapefilepath = os.path.join(platform1_input_folder, platform1 + "_event_distr_at_"+"country"+"_level.shp")
            platform1_event_distr_shapefilepath = os.path.join(platform1_input_folder, platform1 + "_event_distr_at_"+spatial_hierarchy_level+"_level.shp")
            platform2_event_distr_shapefilepath = os.path.join(platform2_input_folder, platform2+"_event_distr_at_"+spatial_hierarchy_level+"_level.shp")
            comparison_map_figure_filepath = os.path.join(output_folder, platform1+"_"+platform2+"_event_distr_at_"+spatial_hierarchy_level+"_level.png")
            #comparison_map_figure_filepath = os.path.join(output_folder, platform1+"_"+platform2+"_event_distr_at_"+spatial_hierarchy_level+"_level.pdf")
            print(platform1_event_distr_shapefilepath)
            comparison_plot_map(platform1_event_distr_shapefilepath, platform2_event_distr_shapefilepath, comparison_map_figure_filepath, limits, continent_name)



