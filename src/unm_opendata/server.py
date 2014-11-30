'''
Created on Oct 5, 2014

@author: lnunno
'''
import cherrypy
from unm_opendata.constants import BASE_DIR
from unm_opendata.jinja_init import env
from unm_opendata import schedule
from unm_opendata import util
from unm_opendata.models import Course
from unm_opendata import db

class UnmOpenDataApp(object):
    
    def __init__(self):
        self.campus = schedule.get_campus('ABQ') 
    
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
    def course(self, subject_code, course_number ):
        template = env.get_template('course.html')
        subject = schedule.get_subject(subject_code, self.campus)
        course = schedule.get_course(course_number, subject)
        course = Course(course)
        backlink = '/subject?code=%s' % (subject[0].attrib['code'])
        return template.render(subject=subject, course=course, backlink=backlink)
    
    @cherrypy.expose
    def search(self, q):
        results = db.search_course(q)
        return results
       
if __name__ == '__main__':
    
    config = {
              '/':{
                   'tools.sessions.on': True,
                   'tools.staticdir.on': True,
                   'tools.staticdir.root': BASE_DIR,
                   'tools.staticdir.dir': 'static'
                   }
              }
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.server.socket_port = 8080
    cherrypy.quickstart(UnmOpenDataApp(), '/', config=config)
