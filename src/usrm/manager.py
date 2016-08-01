import easytrader
import pymongo
from util.db import DB
from util.logger import logger
import logging
import os

_logger = logging.getLogger(__name__)


"""
User Info:
       name : string
       balance : dictionary
       {
        'asset_balance': '资产总值',
        'current_balance': '当前余额',
        'enable_balance': '可用金额',
        'market_value': '证券市值',
        'money_type': '币种',
        'pre_interest': '预计利息'
        }

        position: [dictionary]
        [{'cost_price': '摊薄成本价',
          'current_amount': '当前数量',
          'enable_amount': '可卖数量',
          'income_balance': '摊薄浮动盈亏',
          'keep_cost_price': '保本价',
          'last_price': '最新价',
          'market_value': '证券市值',
          'position_str': '定位串',
          'stock_code': '证券代码',
          'stock_name': '证券名称'}]
"""
class Manager(object):
    USER_INFO_CFG_PATH = "usr_cfg"

    def __init__(self):
        self.__db = DB("user")

        usr_colleciton = self.__db.get_collection('user_base')
        if usr_colleciton is None:
          usr_colleciton = self.__db.create_collection('user_base')
        self.__users = usr_colleciton

    def __is_user_already_exist(self, name):
        result = self.__users.find_one({"UserName" : name})
        if result is not None:
            return True

        return False

    def __get_user_cfg_file(self, name):
        file_name = name + '.json'
        cfg_file = os.path.join(self.USER_INFO_CFG_PATH, file_name)
        print cfg_file
        return cfg_file

    def __get_user_info_from_stock_seller(self, name, stock_seller):
        user = easytrader.use(stock_seller)
        cfg_file = self.__get_user_cfg_file(name) 

        try:
            print cfg_file
            user.prepare(cfg_file)
            user.login()
        except Exception as e:
            print e
            print "login stock seller failed"
            _logger.exception("User login failed")
            return None, None

        _logger.debug("%s login success" % name)

        balance = user.get_balance()
        position = user.get_position()

        return balance, position    

    def __encode_user_db_info(self, user, balance, position):
        user_info = {}
        user_info["UserName"] =  user["UserName"]
        user_info["StockSeller"] = user["StockSeller"]
        user_info["Balance"] = balance
        user_info["Postion"] = position
        return user_info

    def add_user(self, user):
        name = user['UserName']
        if self.__is_user_already_exist(name):
            _logger.warn("add user is already exist, user name is %s" % name)
            return self.get_user(name)

        balance, position = self.__get_user_info_from_stock_seller(name, user["StockSeller"])
        if balance is None or position is None:
            _logger.error("Get user info from stocker seller failed")

        db_user_info = self.__encode_user_db_info(user, balance, position)
        try :
            self.__users.insert_one(db_user_info)
        except Exception as e:
            _logger.exception("Insert user in db is exception")

    def delete_user(self, name):
        result = self.__users.delete_one({'UserName' : name})
        if result.deleted_count != 1:
            print 'delete unexist user'
            _logger.warn('Delete user failed, user name is %s' % name)

    def get_user(self, name):
        user = self.__users.find_one({"UserName" : name})

        return user

    def concern_stock(self, user_name, stock_code):
        pass

    def unconcern_stock(self, user_name, stock_code):
        pass
    
    def add_fake_user(self, user):
        name = user['UserName']
        balance, position = None, None

        db_user_info = self.__encode_user_db_info(user, balance, position)
        try :
            self.__users.insert_one(db_user_info)
        except Exception as e:
            _logger.exception("Insert user in db is exception")

    def get_all_user(self):
        users = []
        for user in self.__users.find():
            print user
            users.append(user)

        return users

    def delete_all_fake(self, fake_user):
        self.__users.delete_many({"UserName" : fake_user["UserName"]})


if __name__ == "__main__":
    user_name = '666626453808'
    manager = Manager()

    # test 1 add user
    basic_info = {"UserName" : user_name, "StockSeller" : "ht"}
    manager.add_user(basic_info)
    user = manager.get_user(user_name)
    if user is not None:
        print "test1 add user success"

    #test 2 delete user
    manager.delete_user(user_name)
    user = manager.get_user(user_name)
    if user is None:
        print "delete user success"

    #test 3 add already exist user
    manager.add_user(basic_info)
    user = manager.get_user(user_name)
    if user is not None:
        print "test 3, add user success"
        print user

    print "add user second time"
    manager.add_user(basic_info)  
    manager.delete_user(user_name)

    #test 4 delete not exist user
    manager.delete_user('unexist')

    #test 5 concern a stock
    # manager.add_user(basic_info)
    # manager.concern_stock(user_name, '000001')
    # manager.delete_user(user_name)

    # #test 6 unconcern stock
    # manager.add_user(basic_info)
    # manager.concern_stock(user_name, '000002')
    # manager.unconcern_stock(user_name, '000002')
    # manager.delete_user(user_name)

    #test 7 get all users
    #clear
    manager.add_user(basic_info)
    fake_user = {"UserName" : "fake_tester", "StockSeller" : "ht"}
    manager.delete_all_fake(fake_user)
    manager.add_fake_user(fake_user)
    users = manager.get_all_user()
    if len(users) == 2:
        print 'get all users success'

    manager.delete_user(user_name)
    manager.delete_all_fake(fake_user)
