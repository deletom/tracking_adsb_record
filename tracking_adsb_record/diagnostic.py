#!/usr/bin/env python
# -*-coding:utf8 -*
import time
from datetime import datetime
from model.init_redis import *
from model.config import *

# On récupère la configuration
objConfig = config()
dictConfig = objConfig.getThis()

# On instancie l'objet Redis
objRedis = initRedis()

while 1:
    print("Iteration without treatment: " + objRedis.get('cpt_NoTreatment').__str__())
    print("Flag Ready for treatment: " + objRedis.get('isReadyForTreatment').__str__())
    print("Number Squawk: " + objRedis.llen('squawk').__str__())
    print("Number Aircraft: " + objRedis.hlen('aircraft').__str__())
    print("Number Flight: " + objRedis.llen('flight').__str__())
    time.sleep( 2 )
