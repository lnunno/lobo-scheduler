'''
Created on Nov 1, 2014

@author: lnunno
'''
from pymongo import MongoClient
import xml.etree.ElementTree as ET
from unm_opendata.constants import SCHED_XML_PATH, BUILDING_JSON_PATH,\
    PERKS_JSON_PATH
import json
from unm_opendata import schedule
from unm_opendata.models import Course, CourseEncoder

client = MongoClient()
db = client.unm_app_db

def save_sample_data():
    '''
    Get all CS classes and save to a pickled object to play with.
    '''
    abq_campus = schedule.get_campus('ABQ')
    cs_dept = schedule.get_department('Computer Science', abq_campus)
    cs_courses = schedule.get_courses(cs_dept)
    colleges = schedule.get_colleges(abq_campus)
    for c in colleges:
        print(c.attrib['name'])
        for d in schedule.get_departments(c):
            print('\t'+d.attrib['name'])
    

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

def load_courses():
    campus = schedule.get_campus()
    courses = [Course(c) for c in campus.findall('.//course')]
    table = db.courses
    encoder = CourseEncoder()
    for c in courses:
        value = encoder.default(c)
        table.save(value)
    
def main():
    load_courses()
    
if __name__ == '__main__':
    main()