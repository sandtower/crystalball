from abc import ABCMeta, abstractmethod
from threading import Timer
from channel.mq_client import MsgQueue, MsgQueueException

class Trigger:
    __metaclass__ = ABCMeta

    @abstractmethod
    def start(self):
        pass
    @abstractmethod
    def stop(self):
        pass


class TimeTrigger(Trigger):
    def __init__(self, interval):
        self.__interval = interval
        self.__mq = MsgQueue()
        self.__usr_manager = None

    def __send_request_strategy(self):
        pass

    def __timer_out_process(self):
        pass

    def __start_timer(self):
       t =  Timer(5, self.__timer_out_process)
       t.start()

    def start(self):
       self.__start_timer()
       pass

    def stop(self):
        self.__mq.stop()
        pass


