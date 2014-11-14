'''
Created on Nov 13, 2014

@author: lnunno
'''

class Course(object):
    
    def __init__(self, data, subject):
        self.subject = subject
        self.subject_name = subject.attrib['name']
        self.subject_code = subject.attrib['code']
        self.data = data
        self.number = data.attrib['number']
        self.title = data.attrib['title']
        self.description = data.find('catalog-description').text
        self.sections = data.findall('section')
        
    def heading(self):
        return '%s %s: %s' % (self.subject_code, self.number, self.title)