What is this?
=============

A proof of concept showing we can connect a [Twisted](http://twistedmatrix.com/) client to a [ZeroMQ](http://www.zeromq.org/) server. Uses a ZeroMQ socket file descriptor with Twisted's reactor.

Thanks to [Eric Allen](https://github.com/epall) for help getting this working.

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
    zeromq: got 4523f3fcafd94d0c8f31217a88346f77 ping
    zeromq: sent 4523f3fcafd94d0c8f31217a88346f77 pong
    gateway: forwarding pong response
    twisted: received pong

It was run inside a virtualenv using Python 2.7 (via MacPorts) and Twisted 10.2.0.

Caveat
======

There is currently a race condition where sometimes the ZMQ_FD triggers and
resets before Twisted notices. ZMQ_EVENTS says the socket is readable, but
Twisted never calls doRead() so we never notice. Its unclear whether this is a
bug in ZeroMQ or condition we have to take care of on the Twisted side. I'm
investigating.

