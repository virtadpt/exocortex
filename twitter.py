#!/usr/bin/env python2

# This is the module that pulls and indexes Twitter feeds.
# By: The Doctor <drwho at virtadpt dot net>

# License: GPLv3

# TODO:
# - Make it possible to add, index, and follow arbitrary numbers of Twitter
# feeds.  One database per feed?  How far can Xapian scale?

# Modules
import json

# Global variables.
database_directory = ''

# Classes

# Helper methods

# Core code

# Attempt to connect to Twitter's API server.  If we can't, stop trying but
# make it possible for the user to search already indexed content.

# For every database in database_directory, instantiate a copy of Compactor()
# and compact the database to free up disk space and make searches more
# efficient.

# If we had to create the database then we have to load content into it by
# downloading the whole timeline in chunks and process the information.

# Go into a loop in which we wait for X minutes or Y seconds and download
# tweets posted since the last time the database was updated.
# For every Twitter feed configured for this instance,
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

