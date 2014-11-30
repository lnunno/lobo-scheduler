'''
Created on Nov 1, 2014

@author: lnunno
'''
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, '../../data/'))
SCHED_XML_PATH = os.path.join(DATA_DIR, 'current.xml')
SCHED_XML_PATH_SPRING2015 = os.path.join(DATA_DIR, 'next1.xml')
SCHED_JSON_PATH = os.path.join(DATA_DIR, 'current.json')

BUILDING_JSON_PATH = os.path.join(DATA_DIR, 'abqbuildings.json')
PERKS_JSON_PATH = os.path.join(DATA_DIR, 'perks.json')


STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, 'static/'))
IMAGE_DIR = os.path.join(STATIC_DIR, 'images')
VIZ_DIR = os.path.join(STATIC_DIR, 'viz')
CAMPUS_IMAGES_DIR = os.path.join(IMAGE_DIR, 'campus_images')
CAMPUS_IMAGE_LIST = os.listdir(CAMPUS_IMAGES_DIR)
