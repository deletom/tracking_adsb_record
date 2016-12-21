#!/usr/bin/python3.4
# -*-coding:utf8 -*

"""
Script des données Redis

Le script passe la clé "flagExecute_reset" à 1.
"""

from datetime import datetime
from model.init_redis import *
from model.sms import *

#Instanciation object Redis
objRedis = initRedis()

#Va contenir le texte du SMS
dataTextSms = ""

print("["+datetime.now().__str__()+"] ADSB-Tracking - Start - Reset.")

#On supprime l'ensemble des clés du serveur Redis
objRedis.flushall()
dataTextSms = "RESET OK"

print("["+datetime.now().__str__()+"] ADSB-Tracking - End - Reset.")

objRedis.set('flagExecute_reset', 1)

# On récupère la configuration
objConfig = config()
dictConfig = objConfig.getThis()

"""
On envoie le SMS pour confirmer la bonne RAZ
"""
objSms = sms()
objSms.sendSMS(dataTextSms)
exit()