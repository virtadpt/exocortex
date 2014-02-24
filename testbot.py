#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: set expandtab tabstop=4 shiftwidth=4 :

# This is the base class for an exocortex bot that:
# - Reads a configuration file for all bots of its type.
# - Reads a configuration file specific to its name.
# - Logs into the XMPP server it considers home base.
# - Logs into a persistent MUC it considers its "war room."
# - Opens a private chat session with its master and prints its on-startup
#   status report as it executes its startup process.
# - Opens any databases it needs.
# - Opens any files it needs.
# - Contacts any other systems and services it needs.
# - Prints its "ready" message to the "war room."
# - Goes into an event loop in which it listens for commands to execute,
#   carries them out, and prints the results to the "war room" or a private
#   chat.

# - If commanded to restart, the bot will run its cleanup-and-shutdown
#   procedure without actually shutting down, and then go into its startup
#   cycle, which will cause it to re-load everything.
# - This can be a command in the MUC, a private command, or a signal from a
#   shell.

# - If commanded to shut down from the MUC, a command over a private channel,
#   or an OS signal, it will go through its cleanup-and-shutdwon procedure,
#   announce that it's going offline, and terminate.

# This base class must be instantiated before it can be turned into a bot.  It
# is designed to be extensible to transform it into a bot of any different
# kind.  The filename of the bot is the name it considers its own.  For
# example, floyd.py means that the bot calls itself Floyd, and listens for
# authorized users calling its name to give it commands.

# Exocortex bots will only accept commands from their master by default.  They
# can be commanded to accept orders from other users waiting in their war
# room.  They can also be commanded to stop responding to orders from other
# users.  They will under no circumstances ignore orders from their master,
# whose username is hardcoded into their configuration file.

# Exocortex bots will eventually be able to recognize each other and pass data
# between one another for analysis, but that's in the future.

# By: The Doctor <drwho at virtadpt dot net>
#     0x807B17C1 / 7960 1CDC 85C9 0B63 8D9F  DD89 3BD8 FF2B 807B 17C1

# License: GPLv3

# Load modules.
import ConfigParser
import os
import resource
import sys
import logging
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
import time

# Global variables.

# Classes.
class ExocortexBot(ClientXMPP):
    """ This is a simple XMPP bot written using the SleekXMPP library which,
    at the moment, logs into an XMPP server listening on the loopback host.
    It's a proof of concept right now which I plan on turning into a class
    that can be instantiated and turned into any kind of bot the user wants. """

    # Class attributes go up here so they're easy to find.
    owner = ""
    botname = ""
    room = ""
    imalive = ""

    """ Initialize the bot when it's instantiated. """
    def __init__(self, owner, botname, jid, password, room, room_announcement,
        imalive):

        self.owner = owner
        self.botname = botname.capitalize()
        self.room = room
        self.room_announcement = room_announcement
        self.imalive = imalive

        # Log into the server.
        ClientXMPP.__init__(self, jid, password)

        # Set appropriate event handlers for this session.  Please note that a
        # single event many be processed by multiple matching event handlers.
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)
        self.add_event_handler("groupchat_message", self.groupchat)
        self.add_event_handler("muc::%s::got_online" % self.room,
            self.muc_online)

        # Register plugins to support XEPs.
        self.register_plugin('xep_0030') # Service discovery
        self.register_plugin('xep_0045') # MUC
        self.register_plugin('xep_0199') # Ping

        # Log into database servers.
        # If database does not exist, create it.
        # If database does exist, check the version of the database schema.
        # If the version of the tables is older then the current one, run the
        #    SQL script to update it.

    """ Event handler the fires whenever an XMPP session starts (i.e., it
    logs into the server on this JID.  You can put just about any session
    initialization code here that you want.  The argument 'event' is an empty
    dict. """
    def start(self, event):
        # Tell the server the bot has initiated a session.
        self.send_presence()
        self.get_roster()

        # Start a private chat with the bot's owner.
        self.send_message(mto=self.owner, mbody="%s is now online." %
            self.botname)

        # Log into the bot's home room.
        joined = self.plugin['xep_0045'].joinMUC(self.room, self.botname,
            wait=True)
        if joined:
            print self.botname + " has successfully joined MUC " + self.room
        else:
            print "There was a problem with " + self.botname + " joining " + self.room

    """ Event handler that fires whenever a message is sent to this JID. The
    argument 'msg' represents a message stanza. """
    def message(self, msg):
        # Potential message types: normal, chat, error, headline, groupchat
        if msg['type'] in ('chat', 'normal'):
            if "what is your name" in msg['body']:
                self.send_message(mto=msg['from'], mbody="My name is %s." % self.botname)

            # If the user asks if the bot is alive, respond.
            if "robots" in msg['body'] and "report" in msg['body']:
                self.send_message(mto=msg['from'], mbody=self.imalive)

            # Return a status report to the user.
            if "status" in msg['body']:
                status = process_status(self.botname)
                self.send_message(mto=msg['from'], mbody=status)

            # If the user tells the bot to terminate, do so.
            if "shut down" in msg['body'] or "shutdown" in msg['body']:
                self.send_message(mto=msg['from'],
                    mbody="%s is shutting down..." % (self.botname))
                self.disconnect(wait=True)
                sys.exit(0)

    """ Event handler that fields messages addressed to the bot when they come
    from a chatroom.  The argument 'msg' represents a message stanza. """
    def groupchat(self, msg):
        # If an incoming message came from the bot, ignore it to prevent an
        # infinite loop.
        if msg['type'] in ('groupchat'):
            if msg['mucnick'] != self.botname and self.botname in msg['body']:
                self.send_message(mto=msg['from'].bare,
                    mbody="I heard that. %s said to me:\n%s" % (msg['mucnick'],
                    msg['body']), mtype='groupchat')

    """ Event handler that reacts to presence stanzas in chatrooms issued
    when a user joins the chat.  The argument 'presence' is a presence
    message. """
    def muc_online(self, presence):
        if presence['muc']['nick'] != self.botname:
            self.send_message(mto=presence['from'].bare,
                mbody=self.room_announcement, mtype='groupchat')

# Helper methods.
""" This method prints out some basic system status information for the user,
should they ask for it. """
def process_status(botname):
    procstat = ""

    # Pick information out of the OS that we'll need later.
    current_pid = os.getpid()
    procfile = "/proc/" + str(current_pid) + "/status"

    # Start assembling the status report.
    status = "Agent %s is fully operational on %s.\n" % (botname, time.ctime())
    status = status + "I am operating from directory %s.\n" % os.getcwd()
    status = status + "My current process ID is %d.\n" % current_pid

    # Pull the /proc/<pid>/status info into a string for analysis.
    try:
        s = open(procfile)
        procstat = s.read()
        s.close()
    except:
        status = status + "I was unable to read my process status info.\n"

    # Determine how much RAM the bot is using.
    memory_utilization = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    status = status + "I am currently using %d KB of RAM.\n" % memory_utilization

    # Get the current system load.
    status = status + "The current system load is %s." % str(os.getloadavg())
    return status

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

    # Read the global configuration file.

    # Read its unique configuration file.  Do this by taking the name of the
    # bot and appending '.conf' to it.  Then load it into a config file parser
    # object which has some defaults set on it.
    config = ConfigParser.ConfigParser()
    config .read(botname + '.conf')

    owner = config.get(botname, 'owner')
    username = config.get(botname, 'username')
    password = config.get(botname, 'password')
    muc = config.get(botname, 'muc')
    muclogin = config.get(botname, 'muclogin')
    imalive = config.get(botname, 'imalive')

    # Figure out how to configure the logger.
    loglevel = config.get(botname, 'loglevel')

    # Log into database servers.
    # If database does not exist, create it.
    # If database does exist, check the version of the database schema.
    # If the version of the tables is older then the current one, run the SQL
    #    script to update it.

    # Open any files the bot needs.

    # Contact any servers and services the bot needs to do its job.

    # Log into the XMPP server.  If it can't log in, try to register an account
    # with the server.  If it's a private server this shouldn't be a problem,
    # else print an error to stderr and ABEND.
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)-8s %(message)s')
    bot = ExocortexBot(owner, botname, username, password, muc, muclogin,
        imalive)

    # Connect to the XMPP server and start processing messages.
    if bot.connect():
        bot.process(block=False)
    else:
        print "ERROR: Unable to connect to XMPP server."
        sys.exit(1)

# Clean up after ourselves.

# Fin.
sys.exit(0)
