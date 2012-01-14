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



class KrailOS(callbacks.Plugin):

    """Add the help for "@plugin help KrailOS" here
    This should describe *how* to use this plugin."""

    def doPrivmsg(self, irc, msg):
        if irc.isChannel(msg.args[0]):
            channel = msg.args[0]
            said = ircmsgs.prettyPrint(msg, showNick=False)
            nick = msg.nick

            __dir__ = os.path.dirname(os.path.abspath(__file__))
            filepath = os.path.join(__dir__, 'opinions.csv')

            opinions = csv.reader(open(filepath, 'rb'))
            for row in opinions:
                # match beginning of string/whitespace word end of string/whitespace
                if re.search('(\W|^)' + row[0].lower() + '(\W|$)', said.lower()) is not None:
                    irc.reply(row[0] + "? " + row[1] + ". " + ','.join(row[2:]))

Class = KrailOS


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
