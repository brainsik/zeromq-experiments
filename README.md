What is this?
=============

A proof of concept showing we can connect a [Twisted](http://twistedmatrix.com/) client to a [ZeroMQ](http://www.zeromq.org/) server. Uses a ZeroMQ socket file descriptor with Twisted's reactor.

Requirements
============

To run these scripts you must use version 2.1.0 (or newer) of ZeroMQ and PyZMQ. The `ZMQ_FD` and `ZMQ_EVENTS` sockopts are not in 2.0.x.

*   [Download the ZeroMQ 2.1.0 development (beta) release](http://www.zeromq.org/intro:get-the-software)
*   [Clone the PyZMQ 2.1.0dev bindings](https://github.com/zeromq/pyzmq/)

To build the PyZMQ bindings from source you'll need to install [Cython](http://pypi.python.org/pypi/Cython/).

Example
=======

This is how you can run these scripts and the output you should see:

    (zmq)$ python zmq_server.py &
    [1] 2216
    (zmq)$ python gateway.py &
    [2] 2217
    (zmq)$ python twisted_client.py
    twisted: sending ping
    gateway: forwarding ping request
    zeromq: got ping
    zeromq: sent pong
    gateway: forwarding pong response
    twisted: received pong

It was run inside a virtualenv using Python 2.7 (via MacPorts) and Twisted 10.2.0.