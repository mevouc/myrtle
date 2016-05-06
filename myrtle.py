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
        ircbot.SingleServerIRCBot.__init__(self, [("irc.epita.rezosup.org",
                                            6667)], "myrtle", "Bilbo's pony")
        self.chans = [ "#spam" ]
        self.adjectives = [ "long", "longue", "dur", "dure", "large", "gros",
                "grosse", "grand", "grande", "infini", "infinie", "imposante",
                "immense", "énorme", "imposant", "démesuré", "démesurée",
                "extraordinaire", "magnifique", "beau", "belle", "soyeux",
                "soyeuse", "doux", "douce" ]
        self.di_exps = [ "dis ", "dit ", "di", "d'i", "dhi", "dy", "dhy", "d'y",
                "d'hi", "d'hy"]
        self.cri_exps = [ "crie ", "cries ", "cri", "cry", "kri", "kry", "qri",
                "qry"]
        self.more_or_less = MoreOrLess()
        self.playing_mol = False
        self.repeating = ""

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

    def command(self, serv, cmd):
        return "!" + serv.get_nickname() + " " + cmd

    def check_more_or_less(self, serv, ev, msg):
        if msg == self.command(serv, "dichotomie"):
            self.playing_mol = True
            self.more_or_less = MoreOrLess()
            serv.privmsg(ev.target(), "0")
        if self.playing_mol:
            if msg == serv.get_nickname() + ": more":
                val = self.more_or_less.more()
                serv.privmsg(ev.target(), val)
            elif msg == serv.get_nickname() + ": less":
                val = self.more_or_less.less()
                serv.privmsg(ev.target(), val)
            elif msg == serv.get_nickname() + ": congratulations!":
                author = irclib.nm_to_n(ev.source())
                serv.privmsg(ev.target(), "Merci " + author)
                self.playing_mol = False

    def check_stop(self, serv, ev, msg):
        if msg == self.command(serv, "stop"):
            if self.playing_mol:
                serv.privmsg(ev.target(), "Stopping more or less")
                self.playing_mol = False
            if self.repeating != "":
                serv.privmsg(ev.target(), "Stopping repeating "
                        + self.repeating)
                self.repeating = ""

    def check_repeat(self, serv, msg):
        tokens = msg.split(" ")
        if len(tokens) > 2:
            if tokens[0] + " " + tokens[1] == self.command(serv, "repeat"):
                self.repeating = irclib.nm_to_n(tokens[2])

    def repeat(self, serv, ev, msg):
        serv.privmsg(ev.target(), msg)

    def check_di(self, serv, ev, msg):
        index = -1
        length = 0
        for di_exp in self.di_exps:
            if index != -1:
                break
            index = msg.rfind(di_exp)
            length = len(di_exp)
        if index == -1:
            return
        end_of_msg = msg[index + length:]
        word = end_of_msg.split(" ")[0]
        if word == "":
            return
        serv.privmsg(ev.target(), maj(word))

    def check_cri(self, serv, ev, msg):
        index = -1
        length = 0
        for cri_exp in self.cri_exps:
            if index != -1:
                break
            index = msg.rfind(cri_exp)
            length = len(cri_exp)
        if index == -1:
            return
        end_of_msg = msg[index + length:]
        word = end_of_msg.split(" ")[0]
        if word == "":
            return
        serv.privmsg(ev.target(), word.upper())

    def on_pubmsg(self, serv, ev):
        # action on public message
        msg = ev.arguments()[0]
        author = irclib.nm_to_n(ev.source())
        if author != serv.get_nickname():
            self.check_welcomes(serv, ev, msg.lower())
            self.check_adjectives(serv, ev, msg.lower())
            self.check_more_or_less(serv, ev, msg.lower())
            self.check_stop(serv, ev, msg.lower())
            if author == self.repeating:
                self.repeat(serv, ev, msg)
            self.check_repeat(serv, msg.lower())
            self.check_di(serv, ev, msg.lower())
            self.check_cri(serv, ev, msg.lower())

    def on_kick(self, serv, ev):
        # action on kick
        self.join_chans()

if __name__ == "__main__":
    Myrtle().start()
