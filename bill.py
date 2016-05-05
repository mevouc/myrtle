import irclib
import ircbot

class Bill(ircbot.SingleServerIRCBot):
    # constructor
    def __init__(self):
        print("constructing")
        ircbot.SingleServerIRCBot.__init__(self, [("irc.rezosup.org", 6667)],
                                            "bill", "Bill")
        serv.privmsg("mevouc", "Test.")
        print("constructed")
    def on_welcome(self, serv, ev):
        print("joining")
        serv.join("#spam")
        print("joined")
    def on_pubmsg(self, serv, ev):
        # action on public message
        serv.privmsg("#spam", "Test.")
#    def on_kick(self, serv, ev):
        # action on kick

if __name__ == "__main__":
    Bill().start()
