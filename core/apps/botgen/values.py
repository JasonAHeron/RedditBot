"""
values in use by several files in the module
"""
import os.path 

# use a hashcode to determine the correct location for a bot with certain
# parameters
def bot_path(hashcode):
    bpath = '%s/../../static/bots/%s.py' % (os.path.dirname(__file__), hashcode)
    return os.path.abspath(bpath)