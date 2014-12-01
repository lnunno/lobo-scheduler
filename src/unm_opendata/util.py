'''
Created on Nov 13, 2014

@author: lnunno
'''
from unm_opendata.constants import VIZ_DIR
import os

def is_new_course_level(prev, current):
    '''
    '''
    return prev[0] != current[0]

def course_level(num):
    return '%s00' % (num[0])
    
def course_level_title(num):
    return '%s00 Level Courses' % (num[0])

def sort_by_attribute(element_list, attribute):
    d = {e.attrib[attribute]:e for e in element_list}
    return [d[key] for key in sorted(d)]

def percent_color(percent):
    '''
    Semantic meaning of a percentage for color.
    '''
    if not percent:
        return 'green'
    percent = float(percent)
    if percent > 75:
        return 'red'
    elif percent > 50:
        return 'yellow'
    else:
        return 'green'

def load_viz_file(filename):
    fp = os.path.join(VIZ_DIR, filename)
    return open(fp).read()
    
