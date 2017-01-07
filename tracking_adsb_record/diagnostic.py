#!/usr/bin/python3.4
# -*-coding:utf8 -*

"""
Script de diagnostique des données stockées sous redis
"""

import time
import logging
from datetime import datetime
from model.init_redis import *
from model.config import *


# On récupère la configuration
objConfig = config()
dictConfig = objConfig.getThis()

# On instancie l'objet Redis
objRedis = initRedis()

# On definit le path du log
logging.basicConfig(filename=objRedis.get('config_path_log').decode("utf-8") + time.strftime('%Y%m%d') + '_diagnostic_adsb.log',level=logging.INFO)

"""
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
"""

logging.info("["+time.strftime('%d/%m/%Y %H:%M:%S')+"] Iteration without treatment: " + objRedis.get('cpt_NoTreatment').__str__())
logging.info("["+time.strftime('%d/%m/%Y %H:%M:%S')+"] Flag Ready for treatment: " + objRedis.get('flagExecute_Treatment').__str__())
logging.info("["+time.strftime('%d/%m/%Y %H:%M:%S')+"] Flag Execute reset: " + objRedis.get('flagExecute_reset').__str__())
logging.info("["+time.strftime('%d/%m/%Y %H:%M:%S')+"] Number Squawk: " + objRedis.llen('squawk').__str__())
logging.info("["+time.strftime('%d/%m/%Y %H:%M:%S')+"] Number Squawk Error: " + objRedis.llen('squawk_error').__str__())
logging.info("["+time.strftime('%d/%m/%Y %H:%M:%S')+"] Number Aircraft: " + objRedis.hlen('aircraft').__str__())
logging.info("["+time.strftime('%d/%m/%Y %H:%M:%S')+"] Number Flight: " + objRedis.llen('flight').__str__())
logging.info("["+time.strftime('%d/%m/%Y %H:%M:%S')+"] Number Alert: " + objRedis.hlen('alert').__str__())

