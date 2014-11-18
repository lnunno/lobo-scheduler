'''
Created on Nov 13, 2014

@author: lnunno
'''
from unm_opendata import util

class Course(object):
    
    def __init__(self, data, subject):
        self.subject = subject
        self.subject_name = subject.attrib['name']
        self.subject_code = subject.attrib['code']
        self.data = data
        self.number = data.attrib['number']
        self.title = data.attrib['title']
        self.description = data.find('catalog-description').text
        self.sections = [Section(s) for s in util.sort_by_attribute(data.findall('section'),'number')]
        
    def heading(self):
        return '%s %s: %s' % (self.subject_code, self.number, self.title)

class MeetingTime(object):
    
    def __init__(self, data):
        self.data = data
    
class Section(object):
    
    def __init__(self, data):
        self.data = data
        self.number = data.attrib['number']
        self.crn = data.attrib['crn']
        enroll_elem = data.find('enrollment')
        wait_elem = data.find('waitlist')
        self.num_enrolled = enroll_elem.text
        self.max_enroll = enroll_elem.attrib['max']
        self.percent_enrolled = min(100,int(self.num_enrolled)/int(self.max_enroll)*100) if int(self.max_enroll) > 0 else 0
        self.num_wait = wait_elem.text
        self.max_wait = wait_elem.attrib['max']
        self.instructors = data.findall('.//instructor')
        self.meeting_times = data.findall('.//meeting-time')
        self.credits = data.find('credits').text
        self.fees = data.find('fees')
#         self.start_time = data.find('start-time').text
#         self.end_time = data.find('end-time').text