'''
Created on Nov 1, 2014

@author: lnunno
'''
from pymongo import MongoClient
import xml.etree.ElementTree as ET
from unm_opendata.constants import SCHED_XML_PATH, BUILDING_JSON_PATH, \
    PERKS_JSON_PATH
import json
from unm_opendata import schedule
from unm_opendata.models import Course, CourseEncoder

client = MongoClient()
db = client.unm_app_db

def load_location_data():
    f = open(BUILDING_JSON_PATH)
    js = json.load(f)
    f.close()
    c = db.buildings
    for b in js:
        c.insert(b)
        
def get_buildings():
    result = db.buildings.find().sort('title')
    return result

def find_building(title):
    result = db.buildings.find({'title':title})
    return result

def search_building(term):
    result = db.buildings.find({ '$text': { '$search': term } }).limit(10)
    return result

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
    courses = [Course(c, semester=schedule.semester) for c in campus.findall('.//course')]
    table = db.courses
    encoder = CourseEncoder()
    for c in courses:
        value = encoder.default(c)
        table.insert(value)

def get_course(subject_code, number):
    return db.courses.find({'subject_code':subject_code, 'number':number})

def search_course(term):
    cursor = db.courses.find({ '$text': { '$search': term } }).limit(10)
    return cursor
        
def load_all():
    load_courses()
    load_location_data()
    load_perks_data()
    
def main():
    load_all()
    
if __name__ == '__main__':
    main()
