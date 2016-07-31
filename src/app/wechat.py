from weixin.weixin import server
from util.logger import setup_logger

import logging

setup_logger('weixin.log')
_logger = logging.getLogger(__name__)

while True:
    try:
        server()
    except Exception as e:
        _logger.exception(e)
