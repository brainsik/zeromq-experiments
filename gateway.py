# encoding: utf-8

import time

import zmq
from twisted.internet import defer, protocol, reactor

context = zmq.Context()


class ZMQClient(object):

    def __init__(self, zsock):
        self.zsock = zsock
        self._fd = self.zsock.getsockopt(zmq.FD)
        self.deferred = None

    def fileno(self):
        return self._fd

    def doRead(self):
        while self.zsock.getsockopt(zmq.EVENTS) & zmq.POLLIN:
            self.zsock.recv()  # header
            data = self.zsock.recv()
            self.deferred.callback(data)

    def send(self, msg):
        self.zsock.send("", zmq.SNDMORE)  # delimiter
        self.zsock.send("ping")
        self.deferred = defer.Deferred()
        return self.deferred

    def connectionLost(self, reason):
        reactor.removeReader(self)
        print "connectionLost:", reason

    def logPrefix(self):
        pass

zsock = context.socket(zmq.XREQ)
zsock.connect("tcp://localhost:2010")
zmq_client = ZMQClient(zsock)


class TwistedServer(protocol.Protocol):

    def dataReceived(self, data):
        print "gateway: forwarding", data, "request"
        deferred = zmq_client.send(data)
        deferred.addCallback(self.respond)

    def respond(self, response):
        print "gateway: forwarding", response, "response"
        self.transport.write(response)

factory = protocol.Factory()
factory.protocol = TwistedServer
reactor.listenTCP(2001, factory)
reactor.addReader(zmq_client)
reactor.run()
