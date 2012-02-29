###
# Copyright (c) 2012, Matt Havener
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import supybot.ircmsgs as ircmsgs
import csv
import os
import re
import time


COOL_DOWN_SECONDS = 60*15
SS_DOWNLOAD_SECONDS = 60*5

class KrailOS(callbacks.Plugin):

    """Add the help for "@plugin help KrailOS" here
    This should describe *how* to use this plugin."""

    def load_opinions(self):
        __dir__ = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(__dir__, 'opinions.csv')
        self.opinions = csv.reader(open(filepath, 'rb'))

    def __init__(self, irc):
        self.__parent = super(KrailOS, self)
        self.__parent.__init__(irc)

        self.lastSent = time.time() - COOL_DOWN_SECONDS
        self.lastPull = time.time() - SS_DOWNLOAD_SECONDS
        self.load_opinions()

    def doPrivmsg(self, irc, msg):
        __dir__ = os.path.dirname(os.path.abspath(__file__))

        if not irc.isChannel(msg.args[0]):
            return 

        curTime = time.time()
        channel = msg.args[0]
        said = ircmsgs.prettyPrint(msg, showNick=False)
        nick = msg.nick

        if said.find("I CALL UPON THE POWER OF THE SPREADSHEET") != -1:
            if (self.lastPull + SS_DOWNLOAD_SECONDS) < curTime:
                irc.reply("loading hacking tools...")
                os.system("cd " + __dir__ + "; ./get_new_opinions.sh")
                irc.reply("hacking tools loaded")
                self.lastPull = time.time()
                self.lastSent = time.time() - COOL_DOWN_SECONDS # allow test
                self.load_opinions()
            else:
                print("ignored %s, %d minutes remain" % 
                    (said, 
                    ((self.lastPull + SS_DOWNLOAD_SECONDS) - curTime)/60))
            return

        didReply = False
        for row in self.opinions:
            # match beginning of string/whitespace word end of string/whitespace
            m = re.search('(\(|\s|^)(' + row[0].lower() + ')(\s|\)|\.|\?|\!|$)', said.lower())
            if m is not None:
                if (self.lastSent + COOL_DOWN_SECONDS) < curTime:
                    irc.reply(m.group(2) + "? " + row[1] + ". " + ','.join(row[2:]))
                    didReply = True
                else:
                    print("ignored %s, %d minutes remain" % 
                        (said, 
                        ((self.lastSent + COOL_DOWN_SECONDS) - curTime)/60))

        if didReply:
            self.lastSent = time.time()

Class = KrailOS


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
