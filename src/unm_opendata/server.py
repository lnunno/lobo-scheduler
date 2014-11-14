'''
Created on Oct 5, 2014

@author: lnunno
'''
import cherrypy
import os
from unm_opendata.jinja_init import env
from unm_opendata import schedule
from unm_opendata.models import Course

class UnmOpenDataApp(object):
    
    def __init__(self):
        self.campus = schedule.get_campus('ABQ') 
    
    @cherrypy.expose
    def index(self):
        template = env.get_template('index.html')
        return template.render()
    
    @cherrypy.expose
    def colleges(self):
        template = env.get_template('colleges.html')
        colleges = schedule.get_colleges(self.campus)
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
    
    @cherrypy.expose
    def subject(self, code):
        template = env.get_template('subject.html')
        subject = schedule.get_subject(code, self.campus)
        courses = schedule.get_courses(subject)
        return template.render(subject=subject[0], courses=courses)
    
    @cherrypy.expose
    def course(self, subject_code, course_number):
        template = env.get_template('course.html')
        subject = schedule.get_subject(subject_code, self.campus)
        course = schedule.get_course(course_number, subject)
        course = Course(course, subject[0])
        backlink = '/subject?code=%s' % (subject[0].attrib['code'])
        return template.render(subject=subject, course=course, backlink=backlink)
    
if __name__ == '__main__':
    base_directory = os.path.dirname(os.path.abspath(__file__))
    
    config = {
              '/':{
                   'tools.sessions.on': True,
                   'tools.staticdir.on': True,
                   'tools.staticdir.root': base_directory,
                   'tools.staticdir.dir': 'static'
                   }
              }
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.quickstart(UnmOpenDataApp(), '/', config=config)
