#!/usr/bin/python3.4
# -*-coding:utf8 -*

"""
Script de diagnostique des données stockées sous redis
"""

import time
from datetime import datetime
from model.init_redis import *
from model.config import *

# On récupère la configuration
objConfig = config()
dictConfig = objConfig.getThis()

# On instancie l'objet Redis
objRedis = initRedis()

print("Iteration without treatment: " + objRedis.get('cpt_NoTreatment').decode("utf-8"))
print("Flag Ready for treatment: " + objRedis.get('flagExecute_Treatment').decode("utf-8"))
print("Flag Execute reset: " + objRedis.get('flagExecute_reset').decode("utf-8"))
print("Number Squawk: " + objRedis.llen('squawk').decode("utf-8"))
print("Number Squawk Error: " + objRedis.llen('squawk_error').decode("utf-8"))
print("Number Aircraft: " + objRedis.hlen('aircraft').decode("utf-8"))
print("Number Flight: " + objRedis.llen('flight').decode("utf-8"))
