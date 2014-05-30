"""
    ____           __    ___ __  ____        __ 
   / __ \___  ____/ /___/ (_) /_/ __ )____  / /_
  / /_/ / _ \/ __  / __  / / __/ __  / __ \/ __/
 / _, _/  __/ /_/ / /_/ / / /_/ /_/ / /_/ / /_  
/_/ |_|\___/\__,_/\__,_/_/\__/_____/\____/\__/  
                                                
       Written by Jason Heron & Nick Wood
                 (c) 2014
                 
application.py

this file contains the main application startup code -- it is imported by 
deploy.py to start the RedditBot application
"""

# Import what we need from Flask
# TODO: optimize these imports. * is evil!
from flask import *
import logging
from logging import Formatter, FileHandler
from forms import *
from botCore import *

# Import blueprints
from apps.botgen.controllers import bpnt_botgen

# Initialize the app
app = Flask(__name__)
app.config.from_object('config')

# Register blueprints
app.register_blueprint(bpnt_botgen)
