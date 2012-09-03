#!/usr/bin/env python2

# TODO:
# - Make it possible to add, index, and follow arbitrary numbers of Twitter
# feeds.  One database per feed?  How far can Xapian scale?

# Modules
import cherrypy
from mako.lookup import TemplateLookup
import xapian

# Constants

# Classes

# Helper methods

# Core code
# Read configuration file.

# See if a database for the Twitter feed exists.  If not, create it with the
# proper schema.

# Schema:
# - @username (relevant for retweets)
# - datestamp
# - permalink
# - body
# - list of hashtags
# - URLs found in body
#   - Need to figure out how to determine whether or not to run them through
#     a URL expander (goo.gl, t.co, ow.ly, et cetera).

# Start up the user interface because it runs in the background in a separate
# thread.
# User interface allows the user to search based upon any or all of the fields
# in the schema.  Not sure how to do this year - drop-downs?  Multiple
# fields, each of which allows Boolean operations?
# Execute a search on the Xapian database.
# Count the number of results.
# Sort the results in descending order based upon timestamps.
# Generate a page of X results (with Y not shown yet) and display them on the
# result page.
# If the first result shown != 0, add a <- Previous link to earlier results.
# If there are more results in the list, add a Next-> link.

# Attempt to connect to Twitter's API server.  If we can't, stop trying but
# make it possible for the user to search already indexed content.

# If we had to create the database then we have to load content into it by
# downloading the whole timeline in chunks and process the information.

# Go into a loop in which we wait for X minutes or Y seconds and download
# tweets posted since the last time the database was updated.
# Get the datestamp of the last tweet added to the database.
# Pull all of the tweets posted since the latest one in the database was
# added.
# For each tweet, dissect it to extract the content and add it to the Xapian
# database.
# After catching up, call the Xapian indexer.
# Go to sleep.

# Clean up after ourselves.
# Close the databases.
# Delete tempfiles.

# Fin.
