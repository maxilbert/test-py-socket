import socketserver
import socket
import logging

#from gevent.queue import Queue


class Recv (socketserver.BaseRequestHandler):
    def handle(self):
        try:
            while True:
                self.data=self.request.recv(1024)
                #print("{} send:".format(self.client_address),self.data)
                logging.info("{} send:".format(self.client_address),self.data)
                if not self.data:
                    logging.info('connection lost')
                    #print("connection lost")
                    break
        except Exception as e:
            logging.info(self.client_address, "连接断开")
        finally:
            self.request.close()
    def setup(self):
        logging.info("before handle,连接建立：", self.client_address)
    def finish(self):
        logging.info("finish run  after handle")



class Send:
    _id = id
    _sockets = dict()

    def __init__ (self, id, addresses):
        self._id = id
        self._sockets = dict()
        print(len(addresses))
        for address in addresses:
            self._sockets[address] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #self._sockets[('localhost', 12000+id)].connect(address)


    def send(self, receiver, msg):
        try:
            self._sockets[receiver].sendall(msg)
        except:
            self._sockets[receiver].connect(receiver)
            self._sockets[receiver].sendall(("abc").encode('utf-8'))






