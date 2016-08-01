from usrm.manager import Manager
from util.db import DB
from trade.trigger import Trigger, TimeTrigger

class Controller(object):
    USER_DB_NAME = "user"
    TRIGGER_INTERVAL = 1   #hour

    def __init__(self):
        self.__user_db = DB(self.USER_DB_NAME)
        self.__usr_manager = Manager(self.__user_db)
        self.__trigger = TimeTrigger(self.__usr_manager, self.TRIGGER_INTERVAL)
        self.__stop = threading.Event()

    def start(self):
        self.__trigger.start()

    def stop(self):
        self.__trigger.stop()
        self.__stop.set()



if __name__ == "__main__":
    controller = Controller()
    controller.start()
