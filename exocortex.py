#!/usr/bin/env python2

# This is the front-end that provides the user interface for the information
# gathering and analysis agents.
# By: The Doctor <drwho at virtadpt dot net>

# License: GPLv3

# Modules
import cherrypy
from mako.lookup import TemplateLookup
import xapian

# Global variables

# Classes

# Helper methods

# Core code
# Read configuration file.

# See if a database for the Twitter feed exists.  If not, create it with the
# proper schema.
# For every directory in database_directory...
# xapian create-or-open directory

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
# thread.A

# User interface allows the user to search based upon any or all of the fields
# in the schema.  Not sure how to do this year - drop-downs?  Multiple
# fields, each of which allows Boolean operations?
# Xapian has the ability to search multiple databases simultaneously, so for
# every database found on startup, open a connection.
# Execute a search on the Xapian database inside a try..except block to catch
# NOTFOUND cases.
# Count the number of results.
# Sort the results in descending order based upon timestamps.
# Generate a page of X results (with Y not shown yet) and display them on the
# result page.
# If the first result shown != 0, add a <- Previous link to earlier results.
# If there are more results in the list, add a Next-> link.
# Close the search connections to the databases.

# Clean up after ourselves.
# Close the databases.
# Delete tempfiles.

# Fin.

