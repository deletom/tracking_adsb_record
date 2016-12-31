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
logging.basicConfig(filename=objRedis.get('config_path_log')+time.strftime('%Y%m%d').__str__()+'_adsb.log',level=logging.DEBUG)

"""
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
"""

logging.info("["+time.strftime('%d/%m/%Y %H:%M:%S').__str__()+"] Iteration without treatment: " + objRedis.get('cpt_NoTreatment').__str__())
logging.info("["+time.strftime('%d/%m/%Y %H:%M:%S').__str__()+"] Flag Ready for treatment: " + objRedis.get('flagExecute_Treatment').__str__())
logging.info("["+time.strftime('%d/%m/%Y %H:%M:%S').__str__()+"] Flag Execute reset: " + objRedis.get('flagExecute_reset').__str__())
logging.info("["+time.strftime('%d/%m/%Y %H:%M:%S').__str__()+"] Number Squawk: " + objRedis.llen('squawk').__str__())
logging.info("["+time.strftime('%d/%m/%Y %H:%M:%S').__str__()+"] Number Squawk Error: " + objRedis.llen('squawk_error').__str__())
logging.info("["+time.strftime('%d/%m/%Y %H:%M:%S').__str__()+"] Number Aircraft: " + objRedis.hlen('aircraft').__str__())
logging.info("["+time.strftime('%d/%m/%Y %H:%M:%S').__str__()+"] Number Flight: " + objRedis.llen('flight').__str__())
