'''
Created on Nov 14, 2021

@author: nejat
'''

from event.host import Host

class Hosts:
  # this class is for multiple hosts

  # host_data is a list of dictionaries, each dict represents a host info
  def __init__(self, host_list = None):
    self.host_list = []
    self.nb_hosts = 0
    if host_list is not None:
      for host_data in host_list:
        h = Host(host_data.get_entry())
        self.add_host_info_if_success(h)
    
   
  def is_host_info_empty(self):
    if self.nb_hosts == 0:
      return True
    return False
  
 
  def add_host_info_if_success(self, host_info): # host_info is of type 'Host' 
    if host_info.is_host_info_empty():
      return # do nothing
    
    is_hierarchical = False
    for exis_host_info in self.host_list:
       if host_info.is_hierarchically_included(exis_host_info) or host_info.hierarchically_includes(exis_host_info):
         is_hierarchical = True
         break
    is_identical = False
    for exis_host_info in self.host_list:
      if host_info.is_identical(exis_host_info):
        is_identical = True
        break
      
    if (not is_hierarchical) and (not is_identical):
      self.host_list.append(host_info)
      self.nb_hosts += 1
      

  def get_entry(self):
    return self.host_list
  
  
  def __repr__(self):
    return(str(self.host_list))


  def __str__(self):
    return(str(self.host_list))
  
  
  

