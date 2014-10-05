'''
Created on Oct 5, 2014

@author: lnunno
'''
from jinja2 import Environment, PackageLoader

env = None

def initialize():
    global env
    env = Environment(loader=PackageLoader('unm_opendata', 'templates'))
