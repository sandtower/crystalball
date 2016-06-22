import zmq
import threading
import time

class MqServer(threading.Thread):
    MAX_RETRY_TIMES = 10
    def __init__(self, port=5460):
        threading.Thread.__init__(self)
        self.__cb = None
        self.__port = port
        self.__context = zmq.Context()
        self.__socket = None
        self.__task = None
        self.__stopped = False

    def set_callback(self, cb):
        self.__cb = cb

    def run(self):
        if self.__task:
            return
        self.__stopped = False
        self.__connect()
        self.recv()

    def __connect(self):
        self.__socket = self.__context.socket(zmq.REP)
        self.__socket.bind("tcp://127.0.0.1:%r" % self.__port)

    def recv(self):
        while not self.__stopped:
            try:
                msg = self.__socket.recv()
                print len(msg)
                self.__cb(msg, self)
            except zmq.ZMQError:
                self.__socket.close()
                self.__connect()

    def stop(self):
        if not self.__task:
            return
        self.__stopped = True
        if self.__task.joinable():
            self.__task.join()

    def send(self, msg):
        exception_times = 0
        while exception_times < self.MAX_RETRY_TIMES:
            try:
                self.__socket.send(msg)
                break
            except zmq.ZMQError:
                self.__retry(exception_times)

    def __retry(self, exception_times):
        exception_times += 1
        if exception_times >= self.MAX_RETRY_TIMES:
            raise MqException("mq exception exceed limit")
        else:
            self.__socket.close()
            self.__connect()

    def serialize_and_send(self, msg):
        exception_times = 0
        while exception_times < self.MAX_RETRY_TIMES:
            try:
                self.__socket.send_json(msg)
                break
            except zmq.ZMQError:
                self.__retry(exception_times)

if __name__ == "__main__":
    def test(msg, server):
        print msg
        server.send(msg)
        
    mq_server = MqServer()
    mq_server.set_callback(test)
    mq_server.start()
    time.sleep(10)
    mq_server.stop()
