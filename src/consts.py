'''
Created on Nov 16, 2021

@author: nejat
'''


NEWS_SURVEILLANCE_PADIWEB = "padiweb"
NEWS_SURVEILLANCE_PROMED = "promed"
NEWS_SURVEILLANCE_HEALTHMAP = "healthmap"
NEWS_DB_EMPRESS_I = "empres-i"




# ====================================================
# FILE NAMES
# ====================================================

PADIWEB_ARTICLES_CSV_FILENAME = "articlesweb"
PADIWEB_ARTICLES_INIT_CSV_FILENAME = "articlesweb_init"

PADIWEB_CLASSIF_LABELS_CSV_FILENAME = "classification_label"
PADIWEB_INFO_EXTRAC_CSV_FILENAME = "extracted_information"
PADIWEB_INFO_EXTRAC_INIT_CSV_FILENAME = "extracted_information_init"

PADIWEB_KEYWORD_CSV_FILENAME = "keyword"
PADIWEB_KEYW_ALIGN_CSV_FILENAME = "keyword_alignment"
PADIWEB_SENTENCES_CSV_FILENAME = "sentences_with_labels"
PADIWEB_EXT_SENTENCES_CSV_FILENAME = "extended_sentences_with_labels"
PADIWEB_SENTENCES_INIT_CSV_FILENAME = "sentences_with_labels_init"

PADIWEB_SIGNAL_CSV_FILENAME = "signal"
PADIWEB_DISEASE_KEYWORDS_FILENAME = "disease_keyword"


PADIWEB_AGG_SENTENCES_CSV_FILENAME = "aggregated_sentences_with_labels"
PADIWEB_RELEVANT_SENTENCES_CSV_FILENAME = "relevant_sentences_with_labels"
PADIWEB_EXT_INFO_EXTR_CSV_FILENAME = "extended_extracted_information"
PADIWEB_EVENT_CANDIDATES = "event_candidates_padiweb"
PADIWEB_EVENTS = "events_padiweb"
PADIWEB_INFO_EXTR_SPATIAL_ENTITIES_CSV_FILENAME = "extr_spatial_entities_info"



HEALTHMAP_ARTICLES_CSV_FILENAME = "articlesweb"
HEALTHMAP_SIGNAL_CSV_FILENAME = "signal"
HEALTHMAP_PATHS_CSV_FILENAME = "paths"
HEALTHMAP_PATHS_AGG_CSV_FILENAME = "paths_agg"
HEALTHMAP_PATHS_SIGNAL_CSV_FILENAME = "paths_signal"
HEALTHMAP_EVENT_CANDIDATES = "event_candidates_healthmap"
HEALTHMAP_EVENTS = "events_healthmap"
EMPRESI_EVENT_CANDIDATES = "event_candidates_empresi"
EMPRESI_EVENTS = "events_empresi"

GEONAMES_HIERARCHY_INFO_FILENAME = "geonames_hierarchy"




# ====================================================
# GRAPH
# ====================================================

# node type
NODE_TYPE_EVENT = "event"
NODE_TYPE_LOC_DISTRICT = "district"
NODE_TYPE_LOC_CITY = "city"
NODE_TYPE_LOC_REGION = "region"
NODE_TYPE_LOC_COUNTRY = "country"
NODE_TYPE_LOC_CONTINENT = "continent"
#NODE_TYPE_DATE = "date"
NODE_TYPE_DISEASE = "disease"
NODE_TYPE_DISEASE_SUBTYPE = "disease subtype"
NODE_TYPE_HOST = "host"
NODE_TYPE_HOST_SUBTYPE = "host subtype"
NODE_TYPE_SYMPTOM = "symptom"
NODE_TYPE_SYMPTOM_SUBTYPE = "symptom subtype"
NODE_TYPE_SOURCE = "source"
NODE_TYPE_POST = "post"

# node attributes
NODE_ATTR_DATE = "date"

# edge type
EDGE_TYPE_REPORTING = "reports/reported-by"
EDGE_TYPE_PUBLISHING = "publishes/published-by"
EDGE_TYPE_WHERE = "where" # >> location
EDGE_TYPE_WHO = "who" # >> host
EDGE_TYPE_WHAT = "what" # >> disease
EDGE_TYPE_HOW = "how" # >> symptom
EDGE_TYPE_HIERARCHY = "hierarchy"
EDGE_TYPE_TEMP_DIST = "temporal-distance"
EDGE_TYPE_COUNTRY_NEIGHBOR = "country-neighbor"
EDGE_TYPE_GEODESIC_DIST = "geodesic-distance"
EDGE_TYPE_TEMP_DIST = "temporal dist"

# edge attributes
EDGE_ATTR_WEIGHT = "weight"
EDGE_ATTR_SIGN = "sign"

# ====================================================
# COLUMN NAMES
# ====================================================
COL_ID = "id"
COL_ARTICLE_ID = "article_id"
COL_ARTICLE_ID_RENAMED = "id_articleweb"
COL_SIGNAL_ID = "signal_id"
COL_SIGNAL_ID_RENAMED = "id_signal"
COL_SIGNAL_DATE = "date_signal"
COL_SIGNAL_REF_EMPRESI = "ref_empresi"
COL_PATH_ID = "path_id"
COL_PATH_ID_RENAMED = "id_path"
COL_SUMMARY = "summary"
COL_LANG = "lang"
#COL_CLASSIF_LABEL = "classification_label"
COL_CLASSIF_LABEL_ID = "classificationlabel_id"
COL_ARTICLE_CLASSIF_LABEL_ID = "a_classificationlabel_id"
COL_SENTENCE_CLASSIF_LABEL_ID = "s_classificationlabel_id"
COL_START = "start"
COL_END = "end"
COL_TEXT = "text"
COl_POS = "position"
COl_TOKEN_INDEX = "token_index"
COl_LENGTH = "length"
COL_TYPE = "type"
COL_LABEL = "label"
COL_VALUE = "value"
COL_TITLE = "title"
COL_SENTENCES = "sentences"
COL_URL = "url"
COL_POST_ID = "post_id"
COL_SOURCE = "source"
COL_DESCR = "description"
COL_NAME = "name"
COL_PUBLISHED_TIME = "published_at"
COL_PROCESSED_TEXT = "processed_text"
COL_KEYW_ID = "keyword_id"
COL_KEYW_TYPE_ID = "keyword_type_id"
COL_ALIGN_KEYW_ID = "aligned_keyword_id"
COL_RSSFEED_ID = "id_rssfeed"
COL_GEONAMES_ID = "geonames_id"
COL_GEONAMS_JSON = "geonames_json"
COL_FROM_AUTO_EXTR = "from_automatic_extraction"
COL_SENTENCE_ID = "sentence_id"
COL_FEATURE_CODE = "feature_code"
COL_COUNTRY = "country"
COL_COUNTRY_ID = "id_country"
COL_COUNTRY_FREQ = "country_freq"
COL_NB_COUNTRY_FREQ = "nb_country"
COL_PUB_COUNTRY = "pub_country"
COL_COUNTRY_ALPHA2_CODE = "Alpha-2 code"
COL_COUNTRY_ALPHA3_CODE = "Alpha-3 code"

COL_LAT = "lat"
COL_LNG = "lng"



COL_LOC_DISTRICT = "district"
COL_LOC_CITY = "city"
COL_LOC_REGION = "region"
COL_LOC_COUNTRY = "country"
COL_LOC_CONTINENT = "continent"
COL_DISEASE = "disease"
COL_DISEASE_SUBTYPE = "disease subtype"
COL_HOST = "host"
COL_HOST_SUBTYPE = "host subtype"
COL_SYMPTOM = "symptom"
COL_SYMPTOM_SUBTYPE = "symptom subtype"

COL_ID_PATH_LIST = "id_path_list"

KEY_GEONAMES_COUNTRY = "country"
KEY_GEONAMES_CODE = "code"
KEY_GEONAMES_NAME = "name"
KEY_GEONAMES_STATE = "state"
KEY_GEONAMES_ADDRESS = "address"


# ====================================================
# API
# ====================================================

GEONAMES_API_USERNAME = "arinik9" # for geonames api
GEONAMES_API_USERNAME2 = "arinik1" # for geonames api
GEONAMES_API_USERNAME3 = "arinik2" # for geonames api
GEONAMES_API_USERNAME4 = "arinik10" # for geonames api
GEONAMES_API_USERNAME5 = "arinik11" # for geonames api
GEONAMES_API_USERNAME6 = "arinik12" # for geonames api
GEONAMES_API_USERNAME7 = "arinik13" # for geonames api
GEONAMES_API_USERNAME8 = "arinik14" # for geonames api



# ====================================================
# EVAL MEASURES
# ====================================================

EVAL_FMEASURE = "fmeasure"
EVAL_PRECISION = "precision"
EVAL_RECALL = "recall"
EVAL_NMI = "nmi"
EVAL_ARI = "ari"
EVAL_RI = "ri"

# ====================================================
# RESULT FILE NAMES
# ====================================================
RESULT_FILENAME_EVENT_CLUSTERING = "event-clustering"
RESULT_FILENAME_NETWORK_ALIGNMENT = "network-alignment"
RESULT_FILENAME_DATAFRAME_ALIGNMENT = "dataframe-alignment"


# ====================================================
# FILE FORMAT
# ====================================================

FILE_FORMAT_CSV = "csv"
FILE_FORMAT_TXT = "txt"
FILE_FORMAT_PNG = "png"
FILE_FORMAT_PDF = "pdf"
FILE_FORMAT_SIGNED_GRAPH = "G"
FILE_FORMAT_GRAPHML = "graphml"



# ====================================================
# DISEASE NAMES
# ====================================================
DISEASE_AVIAN_INFLUENZA = "AI"
DISEASE_WEST_NILE_VIRUS = "WNV"





# ====================================================
# Continents
# ====================================================
CONTINENTS_CODE = ["AF", "NA", "OC", "AN", "AS", "EU", "SA"]
CONTINENTS_NAME = ["Africa", "North America", "Oceania", "Antarctica", "Asia", "Europe", "South America"]


# ====================================================
# GEONAMES
# ====================================================
MAX_NB_LOCS_PER_GEONAMES_REQUEST = 100 # by default from geonames













# DISEASE_KEYWORDS_HIERARCHY_DICT = {}
# DISEASE_KEYWORDS_HIERARCHY_DICT["WNV"] = [
#   {"text": "West Nile Virus", "level": 1, "hierarchy": ("WNV",)},
#   {"text": "WNV", "level": 1, "hierarchy": ("WNV",)},
#   {"text": "WNV-unknown", "level": 2, "hierarchy": ("WNV", "WNV-unknown")}
# ]
# DISEASE_KEYWORDS_HIERARCHY_DICT["AI"] = [
#   {"text": "Avian Influenza", "level": 1, "hierarchy": ("AI",)},
#   {"text": "AI", "level": 1, "hierarchy": ("AI",)},
#   {"text": "AI-unknown", "level": 2, "hierarchy": ("AI", "AI-unknown")},
#   {"text": "hpai", "level": 2, "hierarchy": ("AI", "hpai")},
#   {"text": "lpai", "level": 2, "hierarchy": ("AI", "lpai")},
#   {"text": "h5n1", "level": 3, "hierarchy": ("AI", "hpai", "h5n1")},
#   {"text": "h7n9", "level": 3, "hierarchy": ("AI", "hpai", "h7n9")},
#   {"text": "h5n6", "level": 3, "hierarchy": ("AI", "hpai", "h5n6")},
#   {"text": "h5n8", "level": 3, "hierarchy": ("AI", "hpai", "h5n8")},
#   {"text": "h3", "level": 3, "hierarchy": ("AI", "lpai", "h3")},
#   {"text": "h5", "level": 3, "hierarchy": ("AI", "lpai", "h5")},
#   {"text": "h7", "level": 3, "hierarchy": ("AI", "lpai", "h7")},
#   {"text": "h9", "level": 3, "hierarchy": ("AI", "lpai", "h9")},
#   {"text": "h5n2", "level": 3, "hierarchy": ("AI", "lpai", "h5n2")},
#   {"text": "h5n3", "level": 3, "hierarchy": ("AI", "lpai", "h5n3")},
#   {"text": "h5n4", "level": 3, "hierarchy": ("AI", "lpai", "h5n4")},
#   {"text": "h5n5", "level": 3, "hierarchy": ("AI", "lpai", "h5n5")},
#   {"text": "h5n7", "level": 3, "hierarchy": ("AI", "lpai", "h5n7")},
#   {"text": "h5n9", "level": 3, "hierarchy": ("AI", "lpai", "h5n9")},
#   {"text": "h5n10", "level": 3, "hierarchy": ("AI", "lpai", "h5n10")},
#   {"text": "h7n1", "level": 3, "hierarchy": ("AI", "lpai", "h7n1")},
#   {"text": "h7n2", "level": 3, "hierarchy": ("AI", "lpai", "h7n2")},
#   {"text": "h7n3", "level": 3, "hierarchy": ("AI", "lpai", "h7n3")},
#   {"text": "h7n4", "level": 3, "hierarchy": ("AI", "lpai", "h7n4")},
#   {"text": "h7n5", "level": 3, "hierarchy": ("AI", "lpai", "h7n5")},
#   {"text": "h7n6", "level": 3, "hierarchy": ("AI", "lpai", "h7n6")},
#   {"text": "h7n7", "level": 3, "hierarchy": ("AI", "lpai", "h7n7")},
#   {"text": "h7n8", "level": 3, "hierarchy": ("AI", "lpai", "h7n8")},
#   {"text": "h7n9", "level": 3, "hierarchy": ("AI", "lpai", "h7n9")}
# ]
# for i in [1,2,3,4,6,8,9,10]:
#   c1 = "h"+str(i)
#   for j in range(1,11):
#     c2 = "n"+str(j)
#     d = {"text": c1+c2, "level": 3, "hierarchy": ("AI", "lpai", c1+c2)}
#     DISEASE_KEYWORDS_HIERARCHY_DICT["AI"].append(d)
#
#
#
# HOST_KEYWORDS_HIERARCHY_DICT = {}
# HOST_KEYWORDS_HIERARCHY_DICT["human"] = [
#   #{"text": "man", "level": 1, "hierarchy": ("human", "male")},
#   {"text": "hombre", "level": 1, "hierarchy": ("human", "male")}, # (ES)
#   {"text": "mujer", "level": 1, "hierarchy": ("human", "female")}, # (ES)
#   {"text": "señor", "level": 1, "hierarchy": ("human", "male")}, # (ES)
#   {"text": "niña", "level": 1, "hierarchy": ("human", "female")}, # >> child (ES)
#   {"text": "niño", "level": 1, "hierarchy": ("human", "male")}, # >> child (ES)
#   {"text": "adulto", "level": 1, "hierarchy": ("human", "male")},
#   {"text": "adulta", "level": 1, "hierarchy": ("human", "female")},
#   {"text": "uomo", "level": 1, "hierarchy": ("human", "male")},
#   {"text": "donna", "level": 1, "hierarchy": ("human", "female")},
#   {"text": "bambino", "level": 1, "hierarchy": ("human", "male")},
#   {"text": "bambina", "level": 1, "hierarchy": ("human", "female")},
#   {"text": "homme", "level": 1, "hierarchy": ("human", "male")},
#   {"text": "femme", "level": 1, "hierarchy": ("human", "female")},
#   {"text": "человек", "level": 1, "hierarchy": ("human", "male")}, # man (RU)
#   {"text": "женщина", "level": 1, "hierarchy": ("human", "female")}, # woman (RU)
#   {"text": "boy", "level": 1, "hierarchy": ("human", "male")},
#   {"text": "old male", "level": 1, "hierarchy": ("human", "male")},
#   {"text": "adult male", "level": 1, "hierarchy": ("human", "male")},
#   {"text": "girl", "level": 1, "hierarchy": ("human", "female")},
#   {"text": "woman", "level": 1, "hierarchy": ("human", "female")},
#   {"text": "old female", "level": 1, "hierarchy": ("human", "female")},
#   {"text": "adult female", "level": 1, "hierarchy": ("human", "female")},
#   {"text": "old woman", "level": 1, "hierarchy": ("human", "female")},
#   #{"text": "hospital", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   #{"text": "people", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   #{"text": "death", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   {"text": "humain", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   {"text": "humano", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   {"text": "malato", "level": 0, "hierarchy": ("human", "gender-unknown")}, # (ES) or (IT)
#   {"text": "paciente", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   {"text": "enfant", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   {"text": "adulte", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   {"text": "patient", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   {"text": "ребенок", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   {"text": "пациент", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   {"text": "взрослый", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   {"text": "human case", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   {"text": "human h1n", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   {"text": "human h2n", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   {"text": "human h3n", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   {"text": "human h4n", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   {"text": "human h5n", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   {"text": "human h6n", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   {"text": "human h7n", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   {"text": "human h8n", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   {"text": "human h9n", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   {"text": "human h10n", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   {"text": "case of human", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   {"text": "case of a human", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   {"text": "bird flu in human", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   {"text": "avian influenza in human", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   {"text": "new human infect", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   {"text": "human infection", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   {"text": "human transmission", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   {"text": "human west nile virus infection", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   # {"text": "resident", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   {"text": "child", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   {"text": "patient", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   # {"text": "victim", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   # {"text": "hospital", "level": 0, "hierarchy": ("human", "gender-unknown")},
#   {"text": "human", "level": 0, "hierarchy": ("human", "gender-unknown")}
#   # {"text": "death", "level": 0, "hierarchy": ("human", "gender-unknown")}
# ]
#
#
# HOST_KEYWORDS_HIERARCHY_DICT["mammal"] = [
#   {"text": "seal", "level": 1, "hierarchy": ("arctoidea", "seal")},
#   {"text": "dog", "level": 1, "hierarchy": ("canidae", "dog")},
#   {"text": "fox", "level": 1, "hierarchy": ("canidae", "fox")},
#   {"text": "лисиц", "level": 1, "hierarchy": ("canidae", "fox")},
#   {"text": "mula", "level": 1, "hierarchy": ("equidae", "mule")},
#   {"text": "équidés", "level": 1, "hierarchy": ("equidae", "horse")},
#   {"text": "equino", "level": 1, "hierarchy": ("equidae", "horse")},
#   {"text": "équine", "level": 1, "hierarchy": ("equidae", "horse")},
#   {"text": "llama", "level": 1, "hierarchy": ("camelidae", "llama")},
#   {"text": "alpaca", "level": 1, "hierarchy": ("camelidae", "alpaca")},
#   {"text": "horse", "level": 1, "hierarchy": ("equidae", "horse")},
#   {"text": "donkey", "level": 1, "hierarchy": ("equidae", "donkey")},
#   {"text": "mule", "level": 1, "hierarchy": ("equidae", "mule")},
#   {"text": "equine", "level": 0, "hierarchy": ("equidae", "subtype-unknown")},
#   {"text": "equidae", "level": 0, "hierarchy": ("equidae", "subtype-unknown")},
#   {"text": "arctoidea", "level": 0, "hierarchy": ("arctoidea", "subtype-unknown")},
#   {"text": "canidae", "level": 0, "hierarchy": ("canidae", "subtype-unknown")},
#   {"text": "camelidae", "level": 0, "hierarchy": ("camelidae", "subtype-unknown")}
# ]
# HOST_KEYWORDS_HIERARCHY_DICT["mosquito"] = [
#   {"text": "culex pipiens", "level": 1, "hierarchy": ("mosquito", "culex pipiens")},
#   {"text": "culex tarsalis", "level": 1, "hierarchy": ("mosquito", "culex tarsalis")},
#   {"text": "culex", "level": 0, "hierarchy": ("mosquito", "subtype-unknown")},
#   {"text": "mosquito", "level": 0, "hierarchy": ("mosquito", "subtype-unknown")}
# ]
# HOST_KEYWORDS_HIERARCHY_DICT["avian"] = [
#   {"text": "anatidae", "level": 2, "hierarchy":("wild bird", "duck")},
#   {"text": "buzzard", "level": 2, "hierarchy":("wild bird", "buzzard")},
#   {"text": "wigeon", "level": 2, "hierarchy":("wild bird", "duck")},
#   {"text": "rook", "level": 2, "hierarchy":("wild bird", "crow")},
#   {"text": "falcon", "level": 2, "hierarchy":("wild bird", "falcon")},
#   {"text": "crane", "level": 2, "hierarchy":("wild bird", "crane")},
#   {"text": "eagle", "level": 2, "hierarchy":("wild bird", "eagle")},
#   {"text": "dove", "level": 2, "hierarchy":("wild bird", "dove")},
#   {"text": "lapwing", "level": 2, "hierarchy":("wild bird", "lapwing")},
#   {"text": "magpie", "level": 2, "hierarchy":("wild bird", "crow")},
#   {"text": "great egret", "level": 2, "hierarchy":("wild bird", "heron")},
#   {"text": "shelduck", "level": 2, "hierarchy":("wild bird", "duck")},
#   {"text": "kestrel", "level": 2, "hierarchy":("wild bird", "falcon")},
#   {"text": "kite", "level": 2, "hierarchy":("wild bird", "kite")},
#   {"text": "laridae", "level": 2, "hierarchy":("wild bird", "gull")},
#   {"text": "penguin", "level": 2, "hierarchy":("wild bird", "penguin")},
#   {"text": "seagull", "level": 2, "hierarchy":("wild bird", "gull")},
#   {"text": "gull", "level": 2, "hierarchy":("wild bird", "gull")},
#   {"text": "owl", "level": 2, "hierarchy":("wild bird", "owl")},
#   {"text": "strigidae", "level": 2, "hierarchy":("wild bird", "owl")},
#   {"text": "hawk", "level": 2, "hierarchy":("wild bird", "hawk")},
#   {"text": "accipitridae", "level": 2, "hierarchy":("wild bird", "hawk")},
#   {"text": "flamingo", "level": 2, "hierarchy":("wild bird", "flamingo")},
#   {"text": "phoenicopteridae", "level": 2, "hierarchy":("wild bird", "flamingo")},
#   {"text": "pato", "level": 2, "hierarchy":("wild bird", "duck")},
#   {"text": "codorna", "level": 2, "hierarchy":("wild bird", "quail")}, 
#   {"text": "black swan", "level": 2, "hierarchy": ("wild bird", "swan")},
#   {"text": "wild turkey", "level": 2, "hierarchy":("wild bird", "turkey")},
#   {"text": "pelican", "level": 2, "hierarchy":("wild bird", "pelican")},
#   {"text": "pelecanidae", "level": 2, "hierarchy":("wild bird", "pelican")},
#   {"text": "goose", "level": 2, "hierarchy":("wild bird", "goose")},
#   {"text": "geese", "level": 2, "hierarchy":("wild bird", "geese")},
#   {"text": "mallard", "level": 2, "hierarchy":("wild bird", "mallard")},
#   {"text": "wigeon", "level": 2, "hierarchy":("wild bird", "wigeon")},
#   {"text": "duck", "level": 2, "hierarchy":("wild bird", "duck")},
#   {"text": "crow", "level": 2, "hierarchy":("wild bird", "crow")},
#   {"text": "wild fowl", "level": 2, "hierarchy":("wild bird", "wild fowl")},
#   {"text": "eagle", "level": 2, "hierarchy":("wild bird", "eagle")},
#   {"text": "osprey", "level": 2, "hierarchy":("wild bird", "osprey")},
#   {"text": "ashen", "level": 2, "hierarchy":("wild bird", "ashen")},
#   {"text": "falcon", "level": 2, "hierarchy":("wild bird", "falcon")},
#   {"text": "shorebird", "level": 2, "hierarchy":("wild bird", "shorebird")},
#   {"text": "ave salvaje", "level": 1, "hierarchy":("wild bird", "subtype-unknown")},
#   {"text": "oiseau sauvage", "level": 1, "hierarchy":("wild bird", "subtype-unknown")},
#   {"text": "migratory bird", "level": 1, "hierarchy":("wild bird", "subtype-unknown")},
#   {"text": "aquatic bird", "level": 1, "hierarchy":("wild bird", "subtype-unknown")},
#   {"text": "seabird", "level": 1, "hierarchy":("wild bird", "subtype-unknown")},
#   {"text": "seabird", "level": 1, "hierarchy":("wild bird", "subtype-unknown")},
#   {"text": "waterbird", "level": 1, "hierarchy":("wild bird", "subtype-unknown")},
#   {"text": "water bird", "level": 1, "hierarchy":("wild bird", "subtype-unknown")},
#   {"text": "captive bird", "level": 1, "hierarchy":("wild bird", "subtype-unknown")},
#   {"text": "wild bird", "level": 1, "hierarchy":("wild bird", "subtype-unknown")},
#   {"text": "sparrow", "level": 2, "hierarchy":("domestic bird", "sparrow")},
#   {"text": "passeridae", "level": 2, "hierarchy":("domestic bird", "sparrow")},
#   {"text": "phasianidae", "level": 2, "hierarchy":("domestic bird", "chicken")},
#   {"text": "peru", "level": 2, "hierarchy":("domestic bird", "turkey")},
#   {"text": "страус", "level": 2, "hierarchy":("domestic bird", "ostrich")},
#   {"text": "frango", "level": 2, "hierarchy":("domestic bird", "chicken")},
#   {"text": "native chicken", "level": 2, "hierarchy":("domestic bird", "chicken")},
#   {"text": "fowl", "level": 2, "hierarchy":("domestic bird", "fowl")},
#   {"text": "chicken", "level": 2, "hierarchy":("domestic bird", "chicken")},
#   {"text": "turkey", "level": 2, "hierarchy":("domestic bird", "turkey")},
#   {"text": "house crow", "level": 2, "hierarchy":("domestic bird", "crow")},
#   {"text": "ostrich", "level": 2, "hierarchy":("domestic bird", "ostrich")},
#   {"text": "mute swan", "level": 2, "hierarchy":("domestic bird", "swan")},
#   {"text": "peafowl", "level": 2, "hierarchy":("domestic bird", "peafowl")},
#   {"text": "peacock", "level": 2, "hierarchy":("domestic bird", "peacock")},
#   {"text": "poultry", "level": 1, "hierarchy":("domestic bird", "subtype-unknown")},
#   {"text": "backyard bird", "level": 1, "hierarchy":("domestic bird", "subtype-unknown")},
#   {"text": "terrestrial bird", "level": 1, "hierarchy":("domestic bird", "subtype-unknown")},
#   {"text": "domestic bird", "level": 1, "hierarchy":("domestic bird", "subtype-unknown")},
#   {"text": "bird", "level": 0, "hierarchy":("bird-unknown", "subtype-unknown")},
#   {"text": "avian", "level": 0, "hierarchy":("bird-unknown", "subtype-unknown")},
#   {"text": "aviaire", "level": 0, "hierarchy":("bird-unknown", "subtype-unknown")},
#   {"text": "грипп", "level": 0, "hierarchy":("bird-unknown", "subtype-unknown")},
#   {"text": "oiseau", "level": 0, "hierarchy":("bird-unknown", "subtype-unknown")}
# ]


