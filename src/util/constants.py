class Constants(object):
    HIST_DATA_DB_NAME = 'hist_data'
    HIST_TICK_DB_NAME = 'hist_tick'
    TEST_DATA_DB_NAME = 'test_data'
    TEST_TICK_DB_NAME = 'test_tick'

    BASIC_COLLECTION = 'stock_basic'

    CURRENT_BASIC_QUERY_URL = 'http://qt.gtimg.cn/q=%s'
    REALTIME_BASIC_QUERY_URL = 'http://140.207.127.33/q=%s'
    CURRENT_FLOW_QUERY_URL = 'http://qt.gtimg.cn/q=ff_%s'
    STOCK_CODE_CATEGORIES = [('000001', 'sh'), ('39900', 'sz'), ('60', 'sh'), 
                           ('00', 'sz'), ('300', 'sz')]
    STOCK_INDEX_CODES = ['000001', '399001', '399006']

    FESTIVAL_2016 = ['2016-01-01', '2016-02-08', '2016-02-09', '2016-02-10', '2016-02-11', '2016-02-12', '2016-04-04', '2016-05-02', '2016-06-09', '2016-06-10', '2016-09-15', '2016-09-16', '2016-10-03', '2016-10-04', '2016-10-05', '2016-10-06', '2016-10-07'] 
    FESTIVAL_2015 = ['2015-01-01', '2015-01-02', '2015-02-18', '2015-02-19', '2015-02-20', '2015-02-23', '2015-02-24', '2015-04-06', '2015-05-01', '2015-06-22', '2015-10-01', '2015-10-02', '2015-10-05', '2015-10-06', '2015-10-07']
    
    TOKEN = '73377d7ad026026dea9a5c48b0fac15dc04abce4381852639e5a147511ffbf57'
