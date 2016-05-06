#!/usr/bin/env python2
# -*- coding: utf8 -*-
import irclib
import ircbot
import sys

def maj(string):
    if len(string) == 0:
        return string
    elif len(string) == 1:
        return string.upper()
    else:
        return string[0].upper() + string[1:]

class MoreOrLess():
    def __init__(self):
        self.minimum = -sys.maxint - 1
        self.maximum = sys.maxint
        self.val = 0

    def get_min(self):
        return self.minimum

    def get_max(self):
        return self.maximum

    def more(self):
        self.minimum = self.val
        self.val = (self.minimum + self.maximum) / 2
        return self.val

    def less(self):
        self.maximum = self.val
        self.val = (self.minimum + self.maximum) / 2
        return self.val

class Myrtle(ircbot.SingleServerIRCBot):
    # constructor
    def __init__(self):
        ircbot.SingleServerIRCBot.__init__(self, [("irc.rezosup.org", 6667)],
                                            "myrtle", "Bilbo's pony")
        self.chans = [ "#spam" ]
        self.adjectives = [ "long", "longue", "dur", "dure", "large", "gros",
                "grosse", "grand", "grande", "infini", "infinie", "imposante",
                "immense", "énorme", "imposant", "démesuré", "démesurée",
                "extraordinaire", "magnifique", "beau", "belle", "soyeux",
                "soyeuse", "doux", "douce" ]
        self.more_or_less = MoreOrLess()
        self.playing_mol = False

    def join_chans(self, serv):
        for chan in self.chans:
            if chan == "#spam":
                serv.join(chan)
                serv.privmsg("#spam", "Bonjour")
            else:
                serv.join(chan)

    def on_welcome(self, serv, ev):
        self.join_chans(serv)

    def on_join(self, serv, ev):
        joiner = irclib.nm_to_n(ev.source())
        if (joiner != serv.get_nickname()):
            serv.privmsg(ev.target(), "Bonjour " + joiner)

    def on_part(self, serv, ev):
        parter = irclib.nm_to_n(ev.source())
        serv.privmsg(ev.target(), parter + " va me manquer...") 

    def check_welcome(self, serv, ev, salutation, msg):
        if salutation + " " + serv.get_nickname() in msg:
            author = irclib.nm_to_n(ev.source())
            serv.privmsg(ev.target(), maj(salutation) + " " + author)

    def check_welcomes(self, serv, ev, msg):
        self.check_welcome(serv, ev, "bonjour", msg)
        self.check_welcome(serv, ev, "bonsoir", msg)
        self.check_welcome(serv, ev, "salut", msg)
        self.check_welcome(serv, ev, "coucou", msg)
        self.check_welcome(serv, ev, "salutations", msg)
        self.check_welcome(serv, ev, "wesh", msg)
        self.check_welcome(serv, ev, "yo", msg)

    def check_adjectives(self, serv, ev, msg):
        for adj in self.adjectives:
            if "est " + adj in msg:
                serv.privmsg(ev.target(), "Comme ma queue")

    def check_more_or_less(self, serv, ev, msg):
        if not self.playing_mol:
            if msg == "!" + serv.get_nickname() + " dichotomie":
                self.playing_mol = True
                self.more_or_less = MoreOrLess()
                serv.privmsg(ev.target(), "0")
        else:
            if msg == serv.get_nickname() + ": more":
                val = self.more_or_less.more()
                serv.privmsg(ev.target(), val)
            elif msg == serv.get_nickname() + ": less":
                val = self.more_or_less.less()
                serv.privmsg(ev.target(), val)
            elif msg == serv.get_nickname() + ": congratulations!":
                author = irclib.nm_to_n(ev.source())
                serv.privmsg(ev.target(), "Merci " + author)

    def on_pubmsg(self, serv, ev):
        # action on public message
        msg = ev.arguments()[0].lower()
        self.check_welcomes(serv, ev, msg)
        self.check_adjectives(serv, ev, msg)
        self.check_more_or_less(serv, ev, msg)

    def on_kick(self, serv, ev):
        # action on kick
        self.join_chans()

if __name__ == "__main__":
    Myrtle().start()
