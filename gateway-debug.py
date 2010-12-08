# encoding: utf-8

import time
import uuid
from select import select

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
        print "gateway: !! fd EVENT !!"
        print_status(callLater=False)
        print_status(callLater=False)
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

        self._requests[client_id] = defer.Deferred()
        self._zsock.getsockopt(zmq.EVENTS)
        return self._requests[client_id]

    def connectionLost(self, reason):
        reactor.removeReader(self)
        print "connectionLost:", reason

    def logPrefix(self):
        return ""

zsock = context.socket(zmq.REQ)
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


prev_select = None
prev_events = None
zsock_fd = zsock.getsockopt(zmq.FD)

def print_status(callLater=True):
    global prev_select
    global prev_events

    _select = select([zsock_fd],[zsock_fd],[zsock_fd])
    events = zsock.getsockopt(zmq.EVENTS)

    if events != prev_events or _select != prev_select:
        print "select: REQ is readable:", bool(_select[0])
        print "EVENTS: REQ is readable:", bool(events & zmq.POLLIN)
        prev_select = _select
        prev_events = events
    if callLater:
        reactor.callLater(0, print_status)


factory = protocol.Factory()
factory.protocol = TwistedServer
reactor.listenTCP(2001, factory)
reactor.addReader(zmq_client)
reactor.callLater(0, print_status)
print
print
print "!!! This will pin the CPU, so don't forget to kill it. !!!"
print
reactor.run()
