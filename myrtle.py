#!/usr/bin/env python2
import irclib
import ircbot

class Bill(ircbot.SingleServerIRCBot):
    # constructor
    def __init__(self):
        ircbot.SingleServerIRCBot.__init__(self, [("irc.rezosup.org", 6667)],
                                            "myrtle", "Bilbo's pony")
        self.chans = ["#spam"]

    def join_spam(self, serv):
        serv.join("#spam")
        serv.privmsg("#spam", "Bonjour Corwin")

    def join_chans(self, serv):
        for chan in self.chans:
            if chan == "#spam":
                self.join_spam(serv)
            else:
                serv.join(chan)

    def on_welcome(self, serv, ev):
        self.join_chans(serv)

    def on_pubmsg(self, serv, ev):
        # action on public message
        msg = ev.arguments()[0].lower()
        if "bonjour " + self.get_nickname() in msg:
            author = irclib.nm_to_n(ev.source())
            serv.privmsg("#spam", "Bonjour " + author)
    def on_kick(self, serv, ev):
        # action on kick
        join_chans()

if __name__ == "__main__":
    Bill().start()
