'''
Created on Oct 5, 2014

@author: lnunno
'''
import cherrypy
from unm_opendata.constants import BASE_DIR
from unm_opendata.jinja_init import env
from unm_opendata import schedule
from unm_opendata import util
from unm_opendata.models import Course, Place
from unm_opendata import db
from collections import defaultdict

class UnmOpenDataApp(object):
    
    def ensure_initialized(self):
        if self.need_init:
            self.init_saved()  
            self.need_init = False      
            
    def init_saved(self):
        cherrypy.session['starred'] = defaultdict(bool)  # @UndefinedVariable
        self.starred = cherrypy.session['starred']  # @UndefinedVariable
        
    def __init__(self):
        self.campus = schedule.get_campus('ABQ')
        self.need_init = True
    
    @cherrypy.expose
    def colleges(self):
        template = env.get_template('colleges.html')
        colleges = schedule.get_colleges(self.campus)
        colleges = util.sort_by_attribute(colleges, 'name')
        return template.render(colleges=colleges)
    
    @cherrypy.expose
    def college(self, code):
        template = env.get_template('college.html')
        college = schedule.get_college(code, self.campus)
        departments = schedule.get_departments(college)
        return template.render(college=college, departments=departments)
    
    @cherrypy.expose
    def department(self, code):
        template = env.get_template('department.html')
        department = schedule.get_department(code, self.campus)
        subjects = schedule.get_subjects(department)
        return template.render(department=department, subjects=subjects)
    
    @cherrypy.expose(alias='index')
    def subjects(self):
        template = env.get_template('subjects.html')
        subjects = schedule.get_subjects(self.campus)
        subj_set = set()
        unique_subjs = []
        for s in subjects:
            code = s.attrib['code']
            if code in subj_set:
                continue
            else:
                subj_set.add(code)
                unique_subjs.append(s)
        subjects = unique_subjs
        subjects = util.sort_by_attribute(subjects, 'name')
        return template.render(subjects=subjects)
    
    @cherrypy.expose
    def subject(self, code):
        template = env.get_template('subject.html')
        subject = schedule.get_subject(code, self.campus)
        courses = schedule.get_courses(subject)
        return template.render(subject=subject[0], courses=courses, backlink='/subjects')
    
    @cherrypy.expose
    def course(self, subject_code, course_number):
        self.ensure_initialized() 
        template = env.get_template('course.html')
        subject = schedule.get_subject(subject_code, self.campus)
        course = schedule.get_course(course_number, subject)
        course = Course(course)
        backlink = '/subject?code=%s' % (subject[0].attrib['code'])
        return template.render(subject=subject, course=course, backlink=backlink, is_starred=self.is_starred(subject_code, course_number))
    
    @cherrypy.expose
    def stats(self):
        template = env.get_template('stats.html')
        return template.render()
    
    @cherrypy.expose
    def places(self):
        template = env.get_template('places.html')
        buildings = db.get_buildings()
        return template.render(buildings=buildings)
    
    @cherrypy.expose
    def my_schedule(self):
        self.ensure_initialized()
        saved_classes = []
        for (subj,num),t in self.starred.items():
            if not t:
                continue
            c = db.get_course(subj, num)[0]
            saved_classes.append(c)
        template = env.get_template('my_schedule.html')
        return template.render(saved_classes=saved_classes)
    
    @cherrypy.expose
    def place(self, name, code=None):
        template = env.get_template('place.html')
        place = db.find_building(name)
        if place.count() == 0:
            if code is not None:
                result = db.search_building(code)
                if result.count() > 0:
                    return template.render(place=Place(result[0]))
            raise cherrypy.NotFound("Can not find the specified location.")
        return template.render(place=Place(place[0]))
    
    @cherrypy.expose
    def search(self, q):
        template = env.get_template('search.html')
        results = db.search_course(q)
        return template.render(results=list(results))
    
    @cherrypy.expose(alias='404')
    def not_found(self, status, message, traceback, version):
        template = env.get_template('404.html')
        return template.render()
    
    @cherrypy.expose
    def star(self, subject_code, number):
        self.ensure_initialized()      
        self.starred[(subject_code,number)] = not self.starred[(subject_code,number)]
        for k,v in self.starred.items():
            print(k,v)
    
    def is_starred(self, subject_code, number):
        return self.starred[(subject_code,number)]
        
if __name__ == '__main__':
    
    instance = UnmOpenDataApp()
    
    config = {
              '/':{
                   'tools.sessions.on': True,
                   'tools.staticdir.on': True,
                   'tools.staticdir.root': BASE_DIR,
                   'tools.staticdir.dir': 'static',
                   'error_page.404': instance.not_found
                   }
              }
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.server.socket_port = 8080
    cherrypy.quickstart(instance, '/', config=config)
