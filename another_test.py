#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: set expandtab tabstop=4 shiftwidth=4 :

import ConfigParser
from twitterbot import TwitterBot
import logging
from optparse import OptionParser
import os
import sys

""" Figure out what to set the logging level to.  There isn't a
straightforward way of doing this because Python uses constants that are
actually integers under the hood, and I'd really like to be able to do
something like loglevel = 'logging.' + loglevel.  I can't have a pony,
either.  Takes a string, returns a Python loglevel. """
def process_loglevel(loglevel):
    if loglevel == 'critical':
        return 50
    if loglevel == 'error':
        return 40
    if loglevel == 'warning':
        return 30
    if loglevel == 'info':
        return 20
    if loglevel == 'debug':
        return 10
    if loglevel == 'notset':
        return 0

# Core code...
if __name__ == '__main__':
    # If we're running in a Python environment earlier than v3.0, set the
    # default text encoding to UTF-8 because XMPP requires it.
    if sys.version_info < (3, 0):
        reload(sys)
        sys.setdefaultencoding('utf-8')

    # Determine the name of this bot from its filename (without the file
    # extension, if there is one).
    botname = os.path.basename(__file__).split('.')[0]

    # Instantiate a command line options parser.
    optionparser = OptionParser()

    # Define command line switches for the bot, starting with being able to
    # specify an arbitrary configuration file for a particular bot.
    optionparser.add_option('-c', '--conf', dest='configfile', action='store',
        type='string', help='Specify an arbitrary config file for this bot.  Defaults to botname.conf.')

    # Add a command line option that lets you override the config file's
    # loglevel.  This is for kicking a bot into debug mode without having to
    # edit the config file.
    optionparser.add_option('-l', '--loglevel', dest='loglevel', action='store',
        help='Specify the default logging level of the bot.  Choose from CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET.  Defaults to INFO.')

    # Parse the command line args.
    (options, args) = optionparser.parse_args()

    # Read its unique configuration file.  There is a command line argument
    # for specifying a configuration file, but it default to taking the name
    # of the bot and appending '.conf' to it.  Then load it into a config file
    # parser object.
    config = ConfigParser.ConfigParser()
    if options.configfile:
        config.read(options.configfile)
    else:
        config.read(botname + '.conf')

    # Get configuration options out of whichever configuration file gets used.
    owner = config.get(botname, 'owner')
    username = config.get(botname, 'username')
    password = config.get(botname, 'password')
    muc = config.get(botname, 'muc')
    muclogin = config.get(botname, 'muclogin')
    imalive = config.get(botname, 'imalive')
    function = config.get(botname, 'function')

    # Figure out how to configure the logger.  Start by reading the config
    # file.
    config_log = config.get(botname, 'loglevel').lower()
    if config_log:
        loglevel = process_loglevel(config_log)

    # Then try the command line.
    if options.loglevel:
        loglevel = process_loglevel(options.loglevel.lower())

    # Default to WARNING.
    if not options.loglevel and not loglevel:
        loglevel = logging.WARNING

    # Configure the logger.
    logging.basicConfig(level=loglevel,
        format='%(levelname)-8s %(message)s')

    # Get the filename of the response file from the config file.
    responsefile = config.get(botname, 'responsefile')

    # Determine which of the microblog classes to instantiate.
    microblog_type = config.get(botname, 'type')
    if microblog_type == 'twitter':
        # Load the Twitter API keys from the config file.
        twitter_consumer_key = config.get(botname, 'twitter_consumer_key')
        twitter_consumer_secret = config.get(botname, 'twitter_consumer_secret')
        access_token = config.get(botname, 'access_token')
        access_token_secret = config.get(botname, 'access_token_secret')

        # Instantiate a Twitter bot.
        bot = TwitterBot(owner, botname, username, password, muc, muclogin,
            imalive, responsefile, function, twitter_consumer_key,
            twitter_consumer_secret, access_token, access_token_secret)
    else:
        print "No other kinds of microblog bots are defined yet."
        sys.exit(0)

    # Connect to the XMPP server and start processing messages.
    if bot.connect():
        bot.process(block=False)
    else:
        print "ERROR: Unable to connect to XMPP server."
        sys.exit(1)

# Fin.

