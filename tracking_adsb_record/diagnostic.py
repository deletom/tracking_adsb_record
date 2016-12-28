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

print("Iteration without treatment: " + objRedis.get('cpt_NoTreatment').__str__())
print("Flag Ready for treatment: " + objRedis.get('flagExecute_Treatment').__str__())
print("Flag Execute reset: " + objRedis.get('flagExecute_reset').__str__())
print("Number Squawk: " + objRedis.llen('squawk').__str__())
print("Number Aircraft: " + objRedis.hlen('aircraft').__str__())
print("Number Flight: " + objRedis.llen('flight').__str__())
