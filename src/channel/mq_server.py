import zmq
import threading
import time

from zmq.eventloop import ioloop

class MsgQueueException(Exception):
    def __init__(self, msg):
        self.__msg = msg

    def __str__(self):
        return repr(self.__msg)

class MqServer(threading.Thread):
    def __init__(self, port=5460):
        threading.Thread.__init__(self)
        self.__cb = None
        self.__port = port
        self.__context = zmq.Context()
        self.__socket = None
        self.__ioloop = ioloop.IOLoop.instance()
        self.__stopped = threading.Event()
        self.__initialize()

    def __initialize(self):
        self.__socket = self.__context.socket(zmq.REP)
        self.__socket.bind("tcp://127.0.0.1:%r" % self.__port)

    def set_callback(self, cb):
        self.__cb = cb

    def run(self):
        if self.__stopped.isSet():
            return

        self.__ioloop.add_handler(self.__socket, self.rep_handler, zmq.POLLIN)
        self.__ioloop.start()

    def rep_handler(self, socket, events):
        if self.__cb:
            try:
                msg = socket.recv()
                print msg
                self.__cb(msg, self)
            except zmq.ZMQError:
                self.__socket.close()
                self.__initialize()

    def stop(self):
        self.__stopped.set()
        self.__ioloop.stop()

    def send(self, msg):
        try:
            self.__socket.send(msg)
        except zmq.ZMQError:
            raise MsgQueueException("send to request failed.")

if __name__ == "__main__":
    def test(msg, server):
        print msg
        server.send(msg)
        
    mq_server = MqServer()
    mq_server.set_callback(test)
    mq_server.start()
    time.sleep(10)
    mq_server.stop()
