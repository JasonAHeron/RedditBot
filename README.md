RedditBot
=========

RedditBot is a web application writtenn with the Python Flask web application
framework. Its goal is to allow users to generate Python-based web-crawlers 
which make use of Reddit's API to search for a set of terms inside given 
subreddits.

# Changelog

## 0.1.0 

* Instituting versioning with the major_refactor branch.

* General refactor of the project heirarchy. 

> deploy.py is used to launch the application rather than application.py, which is
> inside core/

> We're doing this because everything in the top-level directory should be related
> to deployment on various platforms rather being application code.

* Using Flask blueprints for controllers

* Putting a standard comment header on the important code files.

# Roadmap

## Improve botfile caching

In order to keep performance efficient, we need to cache botcode files to ensure 
commonly used bots (ie. cats, r/atheism, etc...) are computed once and served 
as files rather than being recomputed every time they're needed.

One problem to counter is ensuring the files that get cached are actually used 
more often than once. For this, we can institute a cronjob that prunes files
daily, weekly, monthly, or whatever makes sense by computing which hashes are 
queried most ofte, and how many of them should be kept. 

At this early stage, the cronjob can simply get rid of files that have only been 
touched once, but in the future a more sophisticated algorithm may be necessary.
Since the data is not relational, we can use key-value storage solutions such as
MongoDB or Redis for this. 
