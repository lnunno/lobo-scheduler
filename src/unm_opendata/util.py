'''
Created on Nov 13, 2014

@author: lnunno
'''

def is_new_course_level(prev,current):
    '''
    '''
    return prev[0] != current[0]

def course_level_title(num):
    return '%s00 Level Courses' % (num[0])

def sort_by_attribute(element_list,attribute):
    d = {e.attrib[attribute]:e for e in element_list}
    return [d[key] for key in sorted(d)]