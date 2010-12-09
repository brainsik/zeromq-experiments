# encoding: utf-8

import asyncore
import zmq

context = zmq.Context()


class zmq_wrapper:

    def __init__(self, sock):
        self._socket = sock
        self._fd = sock.getsockopt(zmq.FD)

    def recv(self, *args):
        return self._socket.recv()

    def send(self, data, *args):
        return self._socket.send(data)

    read = recv
    write = send

    def close(self):
        self._socket.close()

    def fileno(self):
        return self._fd

    def getsockopt(self, *args):
        return self._socket.getsockopt(*args)


class zmq_dispatcher(asyncore.dispatcher):

    def __init__(self, sock, map=None):
        asyncore.dispatcher.__init__(self, None, map)
        self.connected = True
        self.set_socket(sock)

    def set_socket(self, sock):
        self.socket = zmq_wrapper(sock)
        self._zsock = sock
        self._fileno = self.socket.fileno()
        self.add_channel()


class EchoServer(zmq_dispatcher):

    def handle_read(self):
        while self.socket.getsockopt(zmq.EVENTS) & zmq.POLLIN:
            try:
                if self._zsock.socket_type == zmq.XREQ:
                    self._zsock.recv(flags=zmq.NOBLOCK)  # header
                data = self._zsock.recv_multipart(flags=zmq.NOBLOCK)
                self._zsock.send_multipart(data)
            except zmq.ZMQError as e:
                if e.errno != zmq.EAGAIN:
                    raise

sock = context.socket(zmq.REP)
sock.bind("tcp://*:4002")
EchoServer(sock)
asyncore.loop()
