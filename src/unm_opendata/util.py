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
