'''
Created on Nov 14, 2021

@author: nejat
'''

from datetime import datetime
import dateutil.parser as parser

from util import retrieve_time_related_info


class Temporality:

  def __init__(self, t, day_no=None, week_no=None, month_no=None, year=None, season=None, season_no=None):
    if isinstance(t, datetime):
      self.date = t
    elif isinstance(t, str):
      # https://stackoverflow.com/questions/27800775/python-dateutil-parser-parse-parses-month-first-not-day
      # if it starts with year info
      if ("-" in t and len(t.split("-")[0])==4) or ("/" in t and len(t.split("/")[0])==4): 
        self.date = parser.parse(t, dayfirst=False)
      else: # if it starts with day info
        self.date = parser.parse(t, dayfirst=True)
    else:
      self.date = t
      
    if day_no is not None and week_no is not None and month_no is not None and year is not None and season is not None and season_no is not None:
      self.day_no = day_no
      self.week_no = week_no
      self.month_no = month_no
      self.year = year
      self.season = season
      self.season_no = season_no
    else:
      day_no_list, week_no_list, biweek_no_list, biweek_no_list, year_list, season_list = retrieve_time_related_info([self.date])
      self.day_no = day_no_list[0]
      self.week_no = week_no_list[0]
      self.month_no = biweek_no_list[0]
      self.year = year_list[0]
      self.season = season_list[0]
      self.season_no = -1
    self.all_interval_info = {"day_no": self.week_no, "week_no": self.week_no, "month_no": self.month_no, \
                               "year": self.year, "season": self.season, "season_no": self.season_no}
    
    
          
  def get_entry(self):
    return(self.date)

  
  def __repr__(self):
    #return "[" + self.get_entry().isoformat() + "]"
    return self.get_entry().isoformat()
       
  def __str__(self):
    #return "[" + self.get_entry().isoformat() + "]"
    return self.get_entry().isoformat()
 