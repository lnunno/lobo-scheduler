'''
Created on Oct 5, 2014

@author: lnunno
'''
import cherrypy
import os
from unm_opendata.jinja_init import env

class UnmOpenDataApp(object):
    
    @cherrypy.expose
    def index(self):
        template = env.get_template('index.html')
        return template.render()
    
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
    cherrypy.quickstart(UnmOpenDataApp(), '/', config=config)