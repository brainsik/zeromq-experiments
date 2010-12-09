# encoding: utf-8

import asyncore
import zmq


class zmq_wrapper:

    def __init__(self, sock):
        self._socket = sock
        self._fd = sock.getsockopt(zmq.FD)

    def __getattr__(self, name):
        return getattr(self._socket, name)

    def fileno(self):
        return self._fd

    def read(self, *args):
        return self._socket.recv(*args)

    def write(self, *args):
        return self._socket.send(*args)


class zmq_dispatcher(asyncore.dispatcher):

    def __init__(self, sock, map=None):
        asyncore.dispatcher.__init__(self, None, map)
        self.connected = True
        self.set_socket(sock)

    def set_socket(self, sock):
        self.socket = zmq_wrapper(sock)
        self._fileno = self.socket.fileno()
        self.add_channel()


asyncore.zmq_dispatcher = zmq_dispatcher
