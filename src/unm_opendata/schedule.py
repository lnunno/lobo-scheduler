'''
Functions for manipulating the UNM Open Data Schedule.

Created on Nov 8, 2014

@author: lnunno
'''
from lxml import etree as ET  # @UnresolvedImport
from unm_opendata.constants import SCHED_XML_PATH
from unm_opendata.models import Course

xml_file = ET.parse(SCHED_XML_PATH)
root = xml_file.getroot()
semester = root.find('semester').attrib['name']

def get_campus(campus='ABQ'):
    query_str = ".//campus[@code='%s']" % (campus)
    return root.findall(query_str)[0]  # Get all the elements related to ABQ campus.

def get_department(code, elt):
    return elt.findall(".//department[@code='%s']" % (code))[0]

def get_departments(elt):
    return elt.findall(".//department")

def get_subjects(elt):
    return elt.findall(".//subject")

def get_subject(code, elt):
    return elt.findall(".//subject[@code='%s']" % (code))

def get_colleges(elt):
    return elt.findall(".//college")

def get_college(code, elt):
    return elt.findall(".//college[@code='%s']" % (code))[0]

def get_courses(elt):
    if type(elt) is list:
        # List of elements.
        for e in elt:
            for item in e.findall('.//course'):
                yield item
    else:    
        return elt.findall('.//course')

def search_course(search_term, elt):
    search_term = search_term.lower()
    ls = elt.findall('.//course')
    courses = [Course(c) for c in ls]
    for c in courses:
        if c.number and search_term in c.number.lower():
            yield c
        elif c.title and search_term in c.title.lower():
            yield c
        elif c.description and search_term in c.description.lower():
            yield c
    
def get_course(course_number, elt):
    if type(elt) is list:
        # List of elements.
        for e in elt:
            ls = e.findall(".//course[@number='%s']" % (course_number))
            if len(ls) > 0:
                return ls[0]
    else:
        return elt.findall(".//course[@number='%s']" % (course_number))[0]
