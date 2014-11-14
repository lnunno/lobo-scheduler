'''
Created on Oct 5, 2014

@author: lnunno
'''
from jinja2 import Environment
from jinja2.loaders import FileSystemLoader
from unm_opendata import util

env = Environment(loader=FileSystemLoader('templates'))
env.globals.update(util=util)
    
