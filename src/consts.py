'''
Created on Nov 16, 2021

@author: nejat
'''

import user_consts
import os


# ====================================================
# Event-Based Surveillance (EBS) platforms
# ====================================================


NEWS_SURVEILLANCE_PADIWEB = "padiweb"
NEWS_SURVEILLANCE_PROMED = "promed"
NEWS_SURVEILLANCE_HEALTHMAP = "healthmap"
NEWS_DB_WAHIS = "wahis"
#NEWS_DB_EMPRESS_I = "empres-i"
NEWS_DB_UK_APHA = "apha"
NEWS_DB_USA_APHIS = "aphis"



# ====================================================
# FOLDERS
# ====================================================


IN_FOLDER = os.path.join(user_consts.MAIN_FOLDER, "in")
OUT_FOLDER = os.path.join(user_consts.MAIN_FOLDER, "out")
IN_EVENTS_FOLDER = os.path.join(IN_FOLDER, "corpus-events")



# ====================================================
# COLUMN NAMES
# ====================================================
COL_ID = "id"
COL_ARTICLE_ID = "article_id"
COL_TITLE = "title"
COL_SENTENCES = "sentences"
COL_URL = "url"
COL_SOURCE = "source"
COL_PUBLISHED_TIME = "published_at"
COL_GEONAMES_ID = "geonames_id"
COL_GEONAMS_JSON = "geonames_json"
COL_FEATURE_CODE = "feature_code"
COL_COUNTRY = "country"
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



# ====================================================
# FILE FORMAT
# ====================================================

FILE_FORMAT_CSV = "csv"
FILE_FORMAT_TXT = "txt"
FILE_FORMAT_PNG = "png"
FILE_FORMAT_PDF = "pdf"




