RedditBot
=========

RedditBot is a web application writtenn with the Python Flask web application
framework. Its goal is to allow users to generate Python-based web-crawlers 
which make use of Reddit's API to search for a set of terms inside given 
subreddits.

Changelog:

# 0.1.0 

* Instituting versioning with the major_refactor branch.

* General refactor of the project heirarchy. 

> deploy.py is used to launch the application rather than application.py, which is
> inside core/

> We're doing this because everything in the top-level directory should be related
> to deployment on various platforms rather being application code.

* Using Flask blueprints for controllers

* Putting a standard comment header on the important code files.