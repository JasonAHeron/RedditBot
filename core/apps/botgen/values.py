"""
values in use by several files in the module
"""
import os.path 

def bot_path(hashcode):
    return os.path.abspath(
            '%s/../../static/bots/%s.py' % (os.path.dirname(__file__), hashcode)
            )