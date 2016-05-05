#!/usr/bin/env python2
import irclib
import ircbot

def maj(string):
    return string.title()

class Bill(ircbot.SingleServerIRCBot):
    # constructor
    def __init__(self):
        ircbot.SingleServerIRCBot.__init__(self, [("irc.rezosup.org", 6667)],
                                            "myrtle", "Bilbo's pony")
        self.chans = ["#spam"]

    def join_spam(self, serv):
        serv.join("#spam")
        serv.privmsg("#spam", "Bonjour")

    def join_chans(self, serv):
        for chan in self.chans:
            if chan == "#spam":
                self.join_spam(serv)
            else:
                serv.join(chan)

    def on_welcome(self, serv, ev):
        self.join_chans(serv)

    def check_welcome(self, serv, ev, salutation, msg):
        if salutation + " " + serv.get_nickname() in msg:
            author = irclib.nm_to_n(ev.source())
            serv.privmsg(ev.target(), maj(salutation) + " " + author)

    def check_welcomes(self, serv, ev, msg)
        self.check_welcome(serv, ev, "bonjour", msg)
        self.check_welcome(serv, ev, "bonsoir", msg)
        self.check_welcome(serv, ev, "salut", msg)
        self.check_welcome(serv, ev, "coucou", msg)
        self.check_welcome(serv, ev, "salutations", msg)

    def on_pubmsg(self, serv, ev):
        # action on public message
        msg = ev.arguments()[0].lower()
        self.check_welcomes(serv, ev, msg)

    def on_kick(self, serv, ev):
        # action on kick
        self.join_chans()

if __name__ == "__main__":
    Bill().start()
