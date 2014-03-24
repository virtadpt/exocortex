#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: set expandtab tabstop=4 shiftwidth=4 :

# This is an Exocortex helper class that extends Tweepy's StreamListener
# class.  This is necessary because it only works when it's extended with
# custom callback methods.  I've split it off into a separate file because
# that makes it easier to maintain and doesn't require finangling nested
# classes.
# - 

# TODO:
# - 

# By: The Doctor <drwho at virtadpt dot net>
#     0x807B17C1 / 7960 1CDC 85C9 0B63 8D9F  DD89 3BD8 FF2B 807B 17C1

# License: GPLv3
# Pre-requisite modules have their own licenses.

# Load modules.
import Queue
import sys
from tweepy import StreamListener

# Classes.
""" This class extends tweepy.StreamListener() so that it does something with
the data.  Namely, it monitors the stream for certain search terms, and every
time it finds one it pushes it into a multiprocessing queue for later
analysis. """
class TwitterStreamListener(StreamListener):
    # Pointers to objects that this class uses which are part of other classes.
    queue = ""
    terms = []
    communications_channel = ""

    """ Set up a pointer to a queue of tweets higher up in the hierarchy. """
    def __init__(self, queue, terms, communications_channel):
        # Call the constructor for the superclass.
        StreamListener.__init__(self)

        # Set up the pointer to the queue of tweets.
        self.queue = queue
        self.terms = terms
        self.communications_channel = communications_channel

    """ Every time a tweet matching one of the search terms is detected, push
    it into the queue. """
    def on_data(self, data):
        # Every time a tweet that matches one of the search terms comes up,
        # add it to the queue.
        self.queue.put(data)

        # As long as there are entries in list of terms to monitor, return
        # True to keep the thread running.
        if len(self.terms):
            return True
        else:
            # If the list of terms to search for is empty, push a sentinel value
            # of None into the queue to stop everything.
            self.queue.put(None)
            return False

    """ In the event of an error, send a status message to the user. """
    def on_error(self, status):
        print "\n\nError: " + str(status) + "\n\n"
        self.communications_channel.send_message(
            mto=self.communications_channel.owner,
            mbody="An error has occurred while communicating with the Twitter API server: %s" % str(status))

# Core code...
if __name__ == '__main__':
    # Self tests go here...
    sys.exit(0)
# Fin.
