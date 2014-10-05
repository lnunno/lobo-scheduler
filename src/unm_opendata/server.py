'''
Created on Oct 5, 2014

@author: lnunno
'''
import cherrypy
import os

class UnmOpenDataApp(object):
    
    @cherrypy.expose
    def index(self):
        return "Hello world."
    
if __name__ == '__main__':
    base_directory = os.path.dirname(os.path.abspath(__file__))
    
    config = {
              '/':{
                   'tools.sessions.on': True,
                   'tools.staticdir.root': os.path.join(base_directory,'static')
                   }
              }
    cherrypy.quickstart(UnmOpenDataApp(), config=config)