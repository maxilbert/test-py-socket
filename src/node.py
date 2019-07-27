import socket
from gevent.queue import Queue
import socketserver




class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass, get_log, queue = None):
        self.logger = get_log()
        if queue is None:
            self.queue = Queue()
        else:
            self.queue = queue
        socketserver.ThreadingTCPServer.__init__(self, server_address, RequestHandlerClass)


class RecvHandler (socketserver.StreamRequestHandler):

    def setup(self):
        super(RecvHandler, self).setup()
        print("before handle, setup connection " + str(self.client_address))
        #self.server.logger.info("before handle, setup connection " + str(self.client_address))

    def handle(self):
        #buffer = bytearray()
        try:
            while True:
                data = self.rfile.readline().strip()
                #print(data)
                if (data != '' and data):
                    self.server.queue.put(data)
                    print("{} send:".format(self.client_address) + str(data))
                else:
                    print(data)
                    print('syntax error messages')
                    #self.server.error('connection lost')
                    #break
        except Exception as e:
            print(self.client_address, "connect disconnected")
            print(e)
            #self.server.error(self.client_address, "connect disconnected")
        finally:
            self.request.close()

    def finish(self):
        super(RecvHandler, self).finish()
        print("finish run after handle")
        #self.server.logger.info("finish run after handle")


class Send:
    _sockets = dict()

    def __init__ (self, addresses):
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
