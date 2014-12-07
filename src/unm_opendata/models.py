'''
Created on Nov 13, 2014

@author: lnunno
'''
from unm_opendata import util
import time
from json.encoder import JSONEncoder

class Course(object):
    
    def __init__(self, data, semester=''):
        self.semester = semester
        self.subject = data.getparent()
        self.subject_name = self.subject.attrib['name']
        self.subject_code = self.subject.attrib['code']
        self.data = data
        self.number = data.attrib['number']
        self.level = util.course_level(self.number)
        self.title = data.attrib['title']
        self.description = data.find('catalog-description').text
        self.sections = [Section(s) for s in util.sort_by_attribute(data.findall('section'), 'number')]
    
    def __repr__(self, *args, **kwargs):
        return '%s %s: %s' % (self.number, self.title, self.description)
    
    def heading(self):
        return '%s %s: %s' % (self.subject_code, self.number, self.title)

class CourseEncoder(JSONEncoder):
    def default(self, o):
        d = o.__dict__
        d.pop('subject')
        d.pop('data')
        section_encoder = SectionEncoder()
        d['sections'] = [section_encoder.default(s) for s in d['sections']]
        return d

def get_time_obj(text):
    if text:
        time_obj = time.strptime(text, '%H%M')
        return time_obj
    else:
        return text
    
def military_time_str(time_obj):
    if time_obj:
        return ('%02d:%02d' % (time_obj.tm_hour, time_obj.tm_min))
    else:
        return None
    
class MeetingTime(object):
    
    def __init__(self, data):
        self.data = data
        self.start_date = data.find('start-date').text
        self.end_date = data.find('end-date').text
        start_time_obj = get_time_obj(data.find('start-time').text)
        end_time_obj = get_time_obj(data.find('end-time').text)
        self.start_time = military_time_str(start_time_obj)
        self.start_time_hour = start_time_obj.tm_hour if self.start_time else None
        self.start_time_min = start_time_obj.tm_min if self.start_time else None
        self.end_time = military_time_str(end_time_obj)
        self.end_time_hour = end_time_obj.tm_hour if self.end_time else None
        self.end_time_min = end_time_obj.tm_min if self.end_time else None
        self.days = [d.text for d in data.findall('.//day')]
        building_elem = data.find('.//bldg')
        self.building = building_elem.text
        self.building_code = building_elem.attrib['code']
        self.room = data.find('.//room').text if data.find('.//room') is not None else '' 

class MeetingTimeEncoder(JSONEncoder):
    def default(self, o):
        d = o.__dict__
        d.pop('data')
        return d        

class Instructor(object):
    
    def __init__(self, data):
        self.data = data
        self.primary = data.attrib['primary']
        self.first = data.find('first').text
        self.last = data.find('last').text
        self.email = data.find('email').text

class InstructorEncoder(JSONEncoder):
    def default(self, o):
        d = o.__dict__
        d.pop('data')
        return d
            
class Section(object):
    
    def __init__(self, data):
        self.data = data
        self.title = data.find('section-title').text
        self.number = data.attrib['number']
        self.crn = data.attrib['crn']
        enroll_elem = data.find('enrollment')
        wait_elem = data.find('waitlist')
        self.num_enrolled = enroll_elem.text
        self.max_enroll = enroll_elem.attrib['max']
        self.percent_enrolled = min(100, int(self.num_enrolled) / int(self.max_enroll) * 100) if int(self.max_enroll) > 0 else 0
        self.num_wait = wait_elem.text
        self.max_wait = wait_elem.attrib['max']
        self.instructors = [Instructor(i) for i in data.findall('.//instructor')]
        self.meeting_times = [MeetingTime(mt) for mt in data.findall('.//meeting-time')]
        self.credits = data.find('credits').text
        self.fees = data.find('fees').text

class SectionEncoder(JSONEncoder):
    def default(self, o):
        d = o.__dict__
        ie = InstructorEncoder()
        d['instructors'] = [ie.default(i) for i in d['instructors']]
        d.pop('data')
        me = MeetingTimeEncoder()
        d['meeting_times'] = [me.default(mt) for mt in d['meeting_times']]
        return d

class Place(object):
    
    def __init__(self, data):
        self.data = data
        
    def __getattr__(self, attr):
        return self.data[attr]