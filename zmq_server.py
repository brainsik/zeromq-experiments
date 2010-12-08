# encoding: utf-8

import zmq
import time

context = zmq.Context()
zsock = context.socket(zmq.REP)
zsock.bind("tcp://*:2010")

while True:
    client_id, request = zsock.recv_multipart()
    print "zeromq: got", client_id, request
    time.sleep(0.01)
    zsock.send_multipart([client_id, "pong"])
    print "zeromq: sent", client_id, "pong"
