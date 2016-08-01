from abc import ABCMeta, abstractmethod
from usrm.manager import Manager
from trader import Trader
from apscheduler.schedulers.blocking import BlockingScheduler
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
    def __init__(self, user_manager, trade_timer_interval):
        self.__trade_interval = trade_timer_interval
        self.__usr_manager = user_manager
        self.__scheduler = BlockingScheduler(daemonic = False)
        self.__mq = MsgQueue()

    def __start_trade_for_user(self, user):
        print("Start trade for %s" % user["UserName"])
        trader = Trader(user, self.__mq)
        trader.start_trade()
        print("End the trade for %s" % user["UserName"])

    def __trade_job(self):
        users = self.__usr_manager.get_all_user()
        for user in users:
            self.__start_trade_for_user(user)

    def start(self):
        self.__scheduler.add_job(self.__trade_job, 'interval', hours = self.__trade_interval)
        self.__scheduler.start()
        self.__mq.start()

    def stop(self):
        self.__scheduler.shutdown()
        self.__stop()


if __name__ == "__main__":
    pass



