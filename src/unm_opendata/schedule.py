'''
Functions for manipulating the UNM Open Data Schedule.

Created on Nov 8, 2014

@author: lnunno
'''
import xml.etree.ElementTree as ET
from unm_opendata.constants import SCHED_XML_PATH

xml_file = ET.parse(SCHED_XML_PATH)
root = xml_file.getroot()

def get_campus(campus='ABQ'):
    query_str = ".//campus[@code='%s']" % (campus)
    return root.findall(query_str)[0]  # Get all the elements related to ABQ campus.

def get_department(code, elt):
    return elt.findall(".//department[@code='%s']" % (code))[0]

def get_departments(elt):
    return elt.findall(".//department")

def get_colleges(elt):
    return elt.findall(".//college")

def get_college(code, elt):
    return elt.findall(".//college[@code='%s']" % (code))[0]

def get_courses(elt):
    return elt.findall('.//course')

def get_course(course_number, elt):
    return elt.findall(".//course[@number='%s']" % (course_number))[0]
