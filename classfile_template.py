#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: set expandtab tabstop=4 shiftwidth=4 :

# This is an Exocortex subclass that implements MOOFMOOFMOOF.  It interfaces
# with MOOFMOOFMOOF and carries out the following functions:
# - 

# TODO:
# - 

# By: The Doctor <drwho at virtadpt dot net>
#     0x807B17C1 / 7960 1CDC 85C9 0B63 8D9F  DD89 3BD8 FF2B 807B 17C1

# License: GPLv3
# Pre-requisite modules have their own licenses.

# Load modules.
from exocortex import ExocortexBot
import sys

# Classes.
class MOOFMOOFMOOF(ExocortexBot):
    # Class attributes go here so they're easy to find.

    # A list of commands defined on bots descended from this particular class.
    # This list is inherited from the ExocortexBot base class, but is extended
    # to include TwitterBot-specific commands.
    commands = ExocortexBot.commands
    MOOFMOOFMOOF_commands = []
    commands.append(MOOFMOOFMOOF_commands)

# Core code...
if __name__ == '__main__':
    # Self tests go here...
    sys.exit(0)
# Fin.
