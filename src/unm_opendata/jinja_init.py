'''
Created on Oct 5, 2014

@author: lnunno
'''
from jinja2 import Environment
from jinja2.loaders import FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))
    
