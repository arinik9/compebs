import itertools
from event.location import Location
from event.temporality import Temporality
from event.hosts import Hosts
from event.disease import Disease
from event.symptom import Symptom

import json




class Event:
  newid = itertools.count()

  def __init__(self, e_id, article_id, url, source, loc, t, \
                dis, h, sym, title, sentences):
    if e_id != -1:
      self.e_id = e_id
    else:
      self.e_id = next(self.newid)
    
    if not isinstance(article_id, int):
    # TypeError("Only integers are allowed.")
      self.article_id = str(article_id)
    else:
      self.article_id = article_id
    
    if not isinstance(url, str):
      TypeError("Only strings are allowed.")
    self.url = url
    
    if not isinstance(source, str):
      TypeError("Only strings are allowed.")
    self.source = source
    
    if not isinstance(title, str):
      TypeError("Only strings are allowed.")
    self.title = title
    
    if not isinstance(sentences, str):
      TypeError("Only strings are allowed.")
    self.sentences = sentences
    
    if not isinstance(loc, Location):
      TypeError("Only objects of type 'Location' are allowed.")
    self.loc = loc
    
    if not isinstance(t, Temporality):
      TypeError("Only objects of type 'Temporality' are allowed.")
    self.date = t
    
    if not isinstance(dis, Disease):
      TypeError("Only objects of type 'Disease' are allowed.")
    self.disease = dis
    
    if not isinstance(h, Hosts):
      TypeError("Only objects of type 'Host' are allowed.")
    self.host = h
    
    if not isinstance(sym, Symptom):
      TypeError("Only objects of type 'Symptom' are allowed.")
    self.symptom = sym  
    
    



  def get_event_entry(self):
    event_entry = [str(self.e_id), str(self.article_id), self.url, self.source]
    event_entry = event_entry + self.loc.get_entry() + [self.date.__str__()] + [str(self.disease.__str__())] \
                 + [str(self.host)] + self.symptom.get_entry()
    return(event_entry)
  
  


  # def compute_event_similarity(self, event2, event_similarity_strategy:EventDuplicateIdentificationStrategy):
  #   sim_score = event_similarity_strategy.perform_event_similarity(self, event2)
  #   return sim_score



  def __repr__(self):
    return "<Event id: %s, artice id: %s, source: %s, loc: %s, date: %s, disease: %s, host: %s, symptom: %s>" \
       % (str(self.e_id), self.article_id, self.source, self.loc, self.date, self.disease, self.host, self.symptom)
       
  def __str__(self):
    return "<Event id: %s, artice id: %s, source: %s, loc: %s, date: %s, disease: %s, host: %s, symptom: %s>" \
       % (str(self.e_id), self.article_id, self.source, self.loc, self.date, self.disease, self.host, self.symptom)
