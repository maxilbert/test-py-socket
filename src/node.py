import socketserver
import socket
from gevent.queue import Queue
import socketserver


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass, get_log):
        self.logger = get_log()
        self.queue = Queue()
        socketserver.ThreadingTCPServer.__init__(self, server_address, RequestHandlerClass)


class Recv (socketserver.BaseRequestHandler):

    def handle(self):
        try:
            while True:
                data = self.request.recv(2048)
                self.server.queue.put(data)
                print("{} send:".format(self.client_address) + str(data))
                #self.server.logger.info("{} send:".format(self.client_address) + str(data))
                if not data:
                    print('connection lost')
                    #self.server.error('connection lost')
                    break
        except Exception as e:
            print(self.client_address, "connect disconnected")
            #self.server.error(self.client_address, "connect disconnected")
        finally:
            self.request.close()

    def setup(self):
        print("before handle, setup connection " + str(self.client_address))
        #self.server.logger.info("before handle, setup connection " + str(self.client_address))

    def finish(self):
        print("finish run after handle")
        #self.server.logger.info("finish run after handle")


class Send:
    _id = id
    _sockets = dict()

    def __init__ (self, id, addresses):
        self._id = id
        self._sockets = dict()
        for address in addresses:
            self._sockets[address] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, receiver, msg):
        try:
            self._sockets[receiver].sendall(msg)
        except Exception as e:
            try:
                self._sockets[receiver].connect(receiver)
                self._sockets[receiver].sendall(msg)
            except Exception as e1:
                print(e1)
