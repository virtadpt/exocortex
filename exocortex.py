#!/usr/bin/env python2

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

# Global variables.

# Classes.

# Helper methods.

# Core code...

# Read the global configuration file.

# Read its unique configuration file.

# Log into the XMPP server.

# Connect to the MUC.

# Initiate communication session with the user.

# Log into database servers.
# If database does not exist, create it.
# If database does exist, check the version of the database schema.
# If the version of the tables is older then the current one, run the SQL
#    script to update it.

# Open any files the bot needs.

# Contact any servers and services the bot needs to do its job.

# Print its ready message to the war room.

# Set its account status using the appropriate PEPs.

# Go into bot event loop.

# Clean up after ourselves.

# Fin.

