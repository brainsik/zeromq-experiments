# encoding: utf-8

import asyncore
import zmq

context = zmq.Context()


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


class EchoServer(zmq_dispatcher):

    def handle_read(self):
        while self.socket.getsockopt(zmq.EVENTS) & zmq.POLLIN:
            try:
                data = self.socket.recv_multipart(flags=zmq.NOBLOCK)
                self.socket.send_multipart(data)
            except zmq.ZMQError as e:
                if e.errno != zmq.EAGAIN:
                    raise

sock = context.socket(zmq.REP)
sock.bind("tcp://*:4002")
EchoServer(sock)
asyncore.loop()
