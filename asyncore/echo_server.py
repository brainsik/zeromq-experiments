# encoding: utf-8

import zmq
from asyncore_zmq import asyncore

context = zmq.Context()


class EchoServer(asyncore.zmq_dispatcher):

    def handle_read(self):
        while self.socket.getsockopt(zmq.EVENTS) & zmq.POLLIN:
            try:
                data = self.socket.recv_multipart(flags=zmq.NOBLOCK)
                self.socket.send_multipart(data)
            except zmq.ZMQError as e:
                if e.errno != zmq.EAGAIN:
                    raise


def main():
    sock = context.socket(zmq.REP)
    sock.bind("tcp://*:4002")
    EchoServer(sock)
    asyncore.loop()

if __name__ == '__main__':
    main()
