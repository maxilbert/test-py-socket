from node import RecvHandler, Send, Server
import socketserver
import multiprocessing
from multiprocessing import Process
from multiprocessloghandler import MultiprocessHandler
import logging, sys
from gevent.queue import Queue as Queue
import gevent

import time

def get_log():
    formattler = '%(levelname)s - %(name)s - %(asctime)s - %(message)s'
    fmt = logging.Formatter(formattler)
    logger = logging.getLogger()
    #logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(fmt)
    #file_handler = MultiprocessHandler('mylog', when='M')
    #file_handler.setLevel(logging.DEBUG)
    #file_handler.setFormatter(fmt)
    logger.addHandler(stream_handler)
    #logger.addHandler(file_handler)
    return logger


def start_recv(address):
    server = Server(address, RecvHandler, get_log)
    server.serve_forever()


def test():
    #global logger
    #logger = get_log()
    N = 4
    host = "localhost"
    port_base = 12000

    addresses = [(host, port_base + i) for i in range(N)]
    sends = [Send(addresses) for _ in range(N)]

    for i in range(N):
        Process(target=start_recv, kwargs={"address": addresses[i]}).start()
    time.sleep(1)

    for j in range(10):
        for i in range(N):
            msg = ("msg %d\n" % j).encode('utf-8')
            sends[j % 4].send(addresses[i], msg)
            #time.sleep(1)


def test1():
    #global logger
    #logger = get_log()
    N = 4
    host = "localhost"
    port_base = 12000

    addresses = [(host, port_base + i) for i in range(N)]
    sends = [Send(addresses) for _ in range(N)]

    threads = [None]*4
    for i in range(N):
        threads[i] = gevent.spawn(badgers[i].run)

        Process(target=start_recv, kwargs={"address": addresses[i]}).start()
    time.sleep(1)

    for j in range(10):
        for i in range(N):
            msg = ("msg %d\n" % j).encode('utf-8')
            sends[j % 4].send(addresses[i], msg)
            #time.sleep(1)



class Node:
    def __init__(self, address: tuple, addresses: list, queue: Queue) -> None:
        self.address = address
        self.addresses = addresses
        self.N = len(addresses)
        self.ingoing = Process(target=self._start_recv_server, kwargs={"address": address, "queue": queue})
        self.ingoing.start()
        time.sleep(1)
        self.outgoing = Send(addresses)

    def _start_recv_server(self, address: tuple, queue: Queue):
        server = Server(address, RecvHandler, get_log, queue)
        server.serve_forever()

    def _send(self, receiver, msg: bytes):
        self.outgoing.send(receiver, msg)
        time.sleep(0.01)

    def _broadcast(self, msg):
        for each in self.addresses:
            self._send(each, msg)

    def broadcast(self, msg):
        self._broadcast(msg)


def test2():
    N = 4
    host = "localhost"
    port_base = 12000
    addresses = [(host, port_base + i) for i in range(N)]
    queues = {address: Queue() for address in addresses}
    nodes = [Node(address=each, addresses=addresses, queue=queues[each]) for each in addresses]

    for j in range(100):
        msg = ("msg %d\n" % j).encode('utf-8')
        nodes[j%4].broadcast(msg)
    print("all messages sent")


if __name__ == "__main__":
    test1()
