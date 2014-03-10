#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: set expandtab tabstop=4 shiftwidth=4 :

# This is an Exocortex subclass that implements a Twitterbot.  It interfaces
# with Twitter's API and carries out the following functions:

# TODO:
# - Log into the Twitter API application server, download the user's tweets,
#   and archive them so they can be searched.
# - Get replies to the user's account.
# - List trending topics.
# - Pull top/all tweets on trending topics.
# - Monitor trending topics and alert if specific search terms show up in the
#   list.
# - Monitor the activity of a particular user.  Archive the user's tweets for
#   searching.
# - Monitor the stream for a particular hashtag.  Scan for particular users or
#   keywords.
# - Add support for the Statusnet API.
#   Twitter-compatible API: http://status.net/wiki/Twitter-compatible_API

# By: The Doctor <drwho at virtadpt dot net>
#     0x807B17C1 / 7960 1CDC 85C9 0B63 8D9F  DD89 3BD8 FF2B 807B 17C1

# License: GPLv3
# Pre-requisite modules have their own licenses.

# Load modules.
import datetime
from exocortex import ExocortexBot
import os
import string
import sys
import tweepy
from tweepy import StreamListener

# Classes.
""" This class implements an interface to the Twitter API which allows the bot
to extract information from Twitter and post stuff to the user's timeline.
The user must have a Twitter account and must have applied for and received
access tokens for Twitter
(https://dev.twitter.com/docs/auth/obtaining-access-tokens).  The API keys
go in your config file.
"""
class TwitterBot(ExocortexBot):
    # Class attributes go here so they're easy to find.
    # Access keys that cryptographically authenticate requests from a
    # particular user to the Twitter API server.
    twitter_consumer_key = ""
    twitter_consumer_secret = ""

    # OAuth access tokens that identify the application and user to the API
    # server.
    access_token = ""
    access_token_secret = ""

    # OAuth authenticator and API interface objects that connect to the
    # Twitter API application server.
    auth = ""
    api = ""

    # Twitter developer account interface objects.  I don't have a better word
    # to describe this, so that's what it is for now.  Blame the "I'm screwing
    # around with this API" test script I wrote.
    user = ""

    # A list of commands defined on bots descended from this particular class.
    # This list is inherited from the ExocortexBot base class, but is extended
    # to include TwitterBot-specific commands.
    commands = ExocortexBot.commands
    twitterbot_commands = ['twitter status', 'search hashtag/for',
        'post tweet/post to twitter', 'list/find trends']
    commands = commands + twitterbot_commands

    # API error catcher.
    api_error = ""

    # List of Twitter WOEID's that have trending topics.  We need to cache
    # this value for later commands.
    woeid = []

    """ Default constructor for the TwitterBot class.  Inherits much of its
    code from ExocortexBot.__init__(), and in fact calls it to set up the
    basic stuff. """
    def __init__(self, owner, botname, jid, password, room, room_announcement,
        imalive, responsefile, function, twitter_consumer_key,
        twitter_consumer_secret, access_token, access_token_secret):

        # Copy the TwitterBot-specific constructor args into class attributes
        # to make them easier to work with.
        self.twitter_consumer_key = twitter_consumer_key
        self.twitter_consumer_secret = twitter_consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

        # Call the base class' constructor.
        ExocortexBot.__init__(self, owner, botname, jid, password, room,
            room_announcement, imalive, responsefile, function)

        # Authenticate with the Twitter API server.
        self.auth = tweepy.OAuthHandler(self.twitter_consumer_key,
            self.twitter_consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)

        # Create an API interface object.
        self.api = tweepy.API(self.auth)

        # Create an interface to the bot's owner's Twitter dev account.
        try:
            self.send_message(mto=self.owner,
                mbody="Trying to contact Twitter API server.  Please wait...")
            self.user = self.api.me()
        except tweepy.error.TweepError as api_error:
            print "\nERROR: " + api_error.reason + ".  Trying again...\n"
            self.send_message(mto=self.owner,
                mbody="Unable to contact Twitter API server.  Error message: %s.  Retrying..." % api_error.reason)

    """ Event handler that fires whenever a message is sent to this JID. The
    argument 'msg' represents a message stanza.  This method implements
    Twitter-specific commands. """
    def message(self, msg):
        # Potential message types: normal, chat, error, headline, groupchat
        if msg['type'] in ('chat', 'normal'):

            # Extract whom the message came from.
            msg_from = str(msg.getFrom())
            msg_from = string.split(msg_from, '/')[0]

            # If the message did not come from the bot's owner, ignore by
            # bouncing out of this method.
            if msg_from != self.owner:
                return

            # To make parsing easier, lowercase the message body before matching
            # against it.
            message = msg['body'].lower()

            # Parse the message text for commands.
            # Class-specific help message
            if "help" in message:
                self.send_message(mto=msg['from'],
                    mbody="Hello.  My name is %s.  I am an instance of TwitterBot.  In addition to the usual ExocortexBot commands, I also support the following specialized commands:\n\n%s" % (self.botname, self.function, self.commands))
                self.send_message(mto=msg['from'],
                    mbody="You can search Twitter for hashtags or arbitrary terms with the commands 'search hashtag #somehashtag' or 'search for somesearchterm'.")
                self.send_message(mto=msg['from'],
                    mbody="You can post something to Twitter with the commands 'post tweet <140 characters here>' or 'post to twitter <140 characters here>'.")
                return

            # The user wants only the status of the Twitter connection.
            if 'twitter status' in message:
                self.send_message(mto=msg['from'],
                    mbody="Polling Twitter status.  Please wait...")
                status = self._twitter_status()
                self.send_message(mto=msg['from'], mbody=status)
                return

            # The user wants to execute a hashtag search.
            if 'search hashtag' in message or 'search for' in message:
                hashtag = message.split()[-1]
                if hashtag == 'hashtag':
                    self.send_message(mto=self.owner,
                        mbody="No hashtag was specified.")
                    return
                else:
                    self.send_message(mto=self.owner,
                        mbody="Executing search for term %s.  Just a moment." %
                        hashtag)
                hashtag_results = self.api.search(q=hashtag,
                    result_type='recent')
                number_of_results = len(hashtag_results)

                # If nothing came back, bounce.
                if not number_of_results:
                    response = "No results were returned for search on " + hashtag + ".'"
                    self.send_message(mto=self.owner, mbody=response)
                    return
                else:
                    response = str(number_of_results) + " tweets were found."
                    self.send_message(mto=self.owner, mbody=response)

                # Build response to send back to user.
                response = ""
                for tweet in hashtag_results:
                    response_line = "@" + tweet.user.name + ": " + tweet.text + "\n" + "Retweeted " + str(tweet.retweet_count) + " times.\n\n"
                    response = response + response_line
                    print "\n" + response_line

                # Send search results to user via private chat.
                self.send_message(mto=self.owner, mbody=response)

            # The user wants to update their Twitter timeline.
            if 'post tweet' in message or 'post to twitter' in message:
                # Remove the command from the message.
                if 'post tweet' in message:
                    message = message.replace('post tweet', '')
                if 'post to twitter' in message:
                    message = message.replace('post to twitter', '')
                message = message.strip()

                # Do some sanity checking - if the tweet's longer than 140
                # characters, don't bother trying.
                if len(message) > 140:
                    self.send_message(mto=self.owner,
                        mbody="Your message is longer than 140 characters.  I can't post this.")
                    return

                # Post the message to Twitter.
                self.send_message(mto=msg['from'],
                    mbody="Posting message to Twitter.  Please wait...")
                posted_to_twitter = self._post_to_twitter(message)
                if posted_to_twitter == True:
                    self.send_message(mto=self.owner,
                        mbody="Status update successfully posted to Twitter.")
                else:
                    self.send_message(mto=self.owner,
                        mbody="Error - unable to post message to Twitter.")
                return

            # The user wants a list of trending topics on Twitter.
            if 'find trends' in message:
                # Reset the list of WOEID's.
                self.woeid = []

                # Strip the command string out of the message, leaving only
                # the keywords we want to work with.
                message = message.replace('find trends', '')
                message = message.strip()
                location = message.title()
                self.send_message(mto=self.owner,
                    mbody="Searching trending topics on Twitter for %s..." %
                           location)

                # Pull the current database of trending locations around the
                # world from the API server.  This is usually in the ballpark
                # of 100kb.
                try:
                    trending_locations = self.api.trends_available()
                except tweepy.error.TweepError as api_error:
                    self.send_message(mto=self.owner,
                        mbody="Unable to contact Twitter API server.  Error message: %s.  Retrying..." % api_error.reason)
                    return

                # Search for the named location in that database.  There are
                # two possible fields that it can appear in, either in
                # 'country' or in 'name' (which can be either the name of the
                # country or a more specific place in that country).  Store
                # the WOEID's in a list.
                for locale in trending_locations:
                    if locale['country'] == location:
                        if locale['woeid'] not in self.woeid:
                            self.woeid.append(locale['woeid'])
                    if locale['name'] == location:
                        if locale['woeid'] not in self.woeid:
                            self.woeid.append(locale['woeid'])

                # Send a response back to the user.
                if not len(self.woeid):
                    response = "There are currently no trending topics in the " + location + " at this time."
                if len(self.woeid) == 1:
                    response = "There is currently one trending topic in the " + location + " at this time."
                if len(self.woeid) > 1:
                    response = "There are currently " + str(len(self.woeid)) + " trending topics in the " + location + " at this time."
                self.send_message(mto=self.owner, mbody=response)

                # Query the API server for as many trending terms (Twitter
                # limits this to 10) as we can get for every WOEID.
                response = "The following terms are trending in location:\n"
                for locale in self.woeid:
                    try:
                        trends = self.api.trends_place(id=locale)
                    except tweepy.error.TweepError as api_error:
                        self.send_message(mto=self.owner,
                            mbody="Unable to contact Twitter API server.  Error message: %s.  Retrying..." % api_error.reason)
                        return
                    for trend in trends:
                        print "\n\n"
                        print ":: " + str(trend)
                        print "\n\n"
                        #response = response + trend['name'] + ": " + trend['url'] + "\n"
                # Send the response back to the user.
                self.send_message(mto=self.owner, mbody=response)
                return

            # Class-specific commands out of the way, call the message parser of
            # the base class.
            ExocortexBot.message(self, msg)

    """ This method only displays the status of the Twitter API server
    connection.  It can be called by self._process_status() but doesn't have
    to be. """
    def _twitter_status(self):
        number_of_followers = ""
        status = ""

        # Query the number of followers the user's account has.  If the query
        # goes through the Twitter API connection is up.
        try:
            number_of_followers = len(self.api.followers())
        except tweepy.error.TweepError as api_error:
            return "ERROR: " + api_error.reason
        if number_of_followers:
            status = self.botname + " has an active connection to the Twitter API service.\n"

        # Query the number of API requests available in this 60 minute
        # timespan and when the hit counter will reset.
        try:
            limit_status = self.api.rate_limit_status()
        except tweepy.error.TweepError as api_error:
            return "ERROR: " + api_error.reason

        # Assemble the status message to transmit to the bot's owner.
        hits_remaining = limit_status['resources']['application']['/application/rate_limit_status']['remaining']
        hits_reset = limit_status['resources']['application']['/application/rate_limit_status']['reset']
        reset_time = datetime.datetime.fromtimestamp(int(hits_reset)).strftime('%H:%M:%S hours on %Y/%m/%d')
        status = status + "This bot has " + str(hits_remaining) + " API hits remaining until Twitter temporarily cuts it off.\n"
        status = status + "The API hit counter will refresh at " + reset_time + "."
        return(status)

    """ Helper method that posts updates to the bot owner's Twitter feed.
    Returns a success/fail to the callling method.  Surprisingly simple,
    really. """
    def _post_to_twitter(self, message):
        try:
            self.api.update_status(message)
        except tweepy.error.TweepError:
            return False
        return True

# Core code...
if __name__ == '__main__':
    # Self tests go here...
    sys.exit(0)
# Fin.
