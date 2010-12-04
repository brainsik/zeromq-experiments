# encoding: utf-8

import zmq

context = zmq.Context()
zsock = context.socket(zmq.REP)
zsock.bind("tcp://*:2010")

while True:
    data = zsock.recv()
    print "zeromq: got", data
    zsock.send("pong")
    print "zeromq: sent pong"
