'''
Created on Nov 1, 2014

@author: lnunno
'''
import os

BASE_DIR = os.path.dirname(os.path.abspath('.'))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, '../data/'))
SCHED_XML_PATH = os.path.join(DATA_DIR, 'current.xml')
SCHED_JSON_PATH = os.path.join(DATA_DIR, 'current.json')

BUILDING_JSON_PATH = os.path.join(DATA_DIR, 'abqbuildings.json')
PERKS_JSON_PATH = os.path.join(DATA_DIR, 'perks.json')
