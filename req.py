#! /usr/bin/env python
# encoding: utf-8
#
#   Kind of like telnet. Sends stdin to REP server.
#   Good for testing REP echo servers. :-)
#
import sys
import zmq

if not len(sys.argv) == 3:
    print "Usage: %s <host> <port>"
    raise SystemExit(1)
host, port = sys.argv[1:3]

context = zmq.Context()
req = context.socket(zmq.REQ)
req.connect("tcp://{0}:{1}".format(host, port))

try:
    while True:
        line = raw_input()
        req.send(line)
        print req.recv()
except KeyboardInterrupt:
    print
