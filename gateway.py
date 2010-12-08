# encoding: utf-8

import time
import uuid

import zmq
from twisted.internet import defer, protocol, reactor

context = zmq.Context()


class ZMQClient(object):

    def __init__(self, zsock):
        self._zsock = zsock

        self._fd = self._zsock.getsockopt(zmq.FD)
        self._requests = {}

    def fileno(self):
        return self._fd

    def doRead(self):
        while self._zsock.getsockopt(zmq.EVENTS) & zmq.POLLIN:
            try:
                if self._zsock.socket_type == zmq.XREQ:
                    self._zsock.recv(flags=zmq.NOBLOCK)  # header
                client_id, data = self._zsock.recv_multipart(flags=zmq.NOBLOCK)
                self._requests.pop(client_id).callback(data)
            except zmq.ZMQError as e:
                if e.errno != zmq.EAGAIN:
                    raise

    def send(self, msg):
        client_id = uuid.uuid4().hex

        if self._zsock.socket_type == zmq.XREQ:
            self._zsock.send("", zmq.SNDMORE)  # delimiter
        self._zsock.send_multipart([client_id, "ping"])

        # print "gateway: going to sleep"
        # time.sleep(1)
        # print "gateway: waking up"

        self._requests[client_id] = defer.Deferred()
        self._zsock.getsockopt(zmq.EVENTS)
        return self._requests[client_id]

    def connectionLost(self, reason):
        reactor.removeReader(self)
        print "connectionLost:", reason

    def logPrefix(self):
        return ""

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
