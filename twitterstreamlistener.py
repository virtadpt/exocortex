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
import sys
from tweepy import StreamListener

# Classes.
""" This class extends tweepy.StreamListener() so that it does something with
the data.  Namely, it monitors the stream for certain search terms, and every
time it finds one it pushes it into a multiprocessing queue for later
analysis. """
class TwitterStreamListener(StreamListener):
    """ Every time a tweet matching one of the search terms is detected, push
    it into the queue. """
    def on_data(self, data):
        # Every time a tweet that matches one of the search terms comes up,
        # add it to the queue.
        tweets.put(data)

        # As long as there are entries in list of terms to monitor, return
        # True to keep the thread running.
        if len(monitoring_terms):
            return True
        else:
            # If the list of terms to search for is empty, push a sentinel value
            # of None into the queue to stop everything.
            tweets.put(None)
            return False

    """ In the event of an error, print a status message to the console. """
    def on_error(self, status):
        print status

""" This is a helper function which runs in a separate thread.  It processes
the queue of matching tweets by picking out useful information and sending it
to the bot's owner. """
def tweet_queue_processor(queue):
    while True:
        print "Picking a tweet out of the queue."
        tweet = queue.get()

        # Detect 'None' as a termination sentinel in the queue.
        if tweet is None:
            print "Queue is now empty."
            break
        else:
            # Process the queue entry.
            print "Queue now contains " + str(queue.qsize()) + " items."
            tweet = json.loads(tweet)
            #print tweet['text']
            user_profile = tweet['user']
            print user_profile['id_str']
            print user_profile['description']
            print user_profile['location']
            print user_profile['geo_enabled']
            print user_profile['name']
            print user_profile['screen_name']
            print user_profile['url']
            print user_profile['time_zone']
            #print tweet['created_at']
            print "\n"

    # All done.  Bail.
    queue.task_done()

# Core code...
if __name__ == '__main__':
    # Self tests go here...
    sys.exit(0)
# Fin.
