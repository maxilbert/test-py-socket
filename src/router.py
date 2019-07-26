from node import RecvHandler, Send, Server
import socketserver
import multiprocessing
from multiprocessing import Process
from multiprocessloghandler import MultiprocessHandler
import logging, sys

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
    sends = [Send(i, addresses) for i in range(N)]

    for i in range(N):
        Process(target=start_recv, kwargs={"address": addresses[i]}).start()
    time.sleep(1)

    for j in range(10):
        for i in range(N):
            msg = ("msg %d\n" % j).encode('utf-8')
            sends[j % 4].send(addresses[i], msg)
            #time.sleep(1)


if __name__ == "__main__":
    test()
