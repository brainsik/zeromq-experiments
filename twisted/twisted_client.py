# encoding: utf-8

from twisted.internet import reactor, protocol

class TwistedClient(protocol.Protocol):
    def connectionMade(self):
        print "twisted: sending ping"
        self.transport.write("ping")

    def dataReceived(self, data):
        print "twisted: received", data
        reactor.callLater(0, self.connectionMade)


factory = protocol.ClientFactory()
factory.protocol = TwistedClient
reactor.connectTCP("localhost", 2001, factory)
reactor.run()
