'''
Created on Nov 1, 2014

@author: lnunno
'''
from pymongo import MongoClient
import xml.etree.ElementTree as ET
from unm_opendata.constants import SCHED_XML_PATH, BUILDING_JSON_PATH,\
    PERKS_JSON_PATH
import json

client = MongoClient()
db = client.unm_app_db

def load_schedule_data():
    sx = ET.parse(SCHED_XML_PATH)
    root = sx.getroot()
    abq_campus = root.findall(".//campus[@code='ABQ']")[0]

def load_location_data():
    f = open(BUILDING_JSON_PATH)
    js = json.load(f)
    f.close()
    c = db.buildings
    for b in js:
        c.insert(b)

def load_perks_data():
    f = open(PERKS_JSON_PATH)
    js = json.load(f)
    js = js['perks']['perk']
    f.close()
    c = db.perks
    for i in js:
        c.insert(i)
    
def main():
    pass
    
if __name__ == '__main__':
    main()