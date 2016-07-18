from usrm.manager import Manager
from util.db import DB, Collection
from trade.trigger import Trigger, TimeTrigger

class Controller(object):
    USER_DB_NAME = "user"
    TRIGGER_INTERVAL = 5

    def __init__(self):
        self.__user_db = DB(self.USER_DB_NAME)
        self.__usr_manager = Manager(self.__user_db)
        self.__trigger = TimeTrigger(self.TRIGGER_INTERVAL)

    def start(self):
        self.__trigger.start()
        self.__usr_manager.start()

    def stop(self):
        self.__trigger.stop()
        self.__usr_manager.stop()



if __name__ == "__main__":
    controller = Controller()
    controller.start()
