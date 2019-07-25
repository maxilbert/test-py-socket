from node import Recv, Send
import socketserver
from multiprocessing import Process
import time

def start_recv(address):
    server = socketserver.TCPServer(address, Recv)
    server.serve_forever()


if __name__ == "__main__":

    N = 4
    addresses=[None]*4

    sends=[None]*4
    host = "localhost"
    port_base = 12000


    for i in range(N):
        addresses[i] = (host, port_base + i)

    for i in range(N):
        sends[i] = Send(i, addresses)
        Process(target=start_recv, kwargs={"address":addresses[i]}).start()

    for j in range(10):
        for i in range(N):
            print('node %d' % i)
            msg = ("msg %d" % j).encode('utf-8')
            sends[j%4].send(addresses[i], msg)
            time.sleep(1)
