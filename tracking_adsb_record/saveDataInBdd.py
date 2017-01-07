#!/usr/bin/python3.4
# -*-coding:utf8 -*

"""
Script d'initialisation des éléments Redis permettant le fonctionnement du script "main.py"
3 phases principales
- Récupération des éléments de configuration (BDD, Redis, URL Dump1090)
- L'ensemble des codes transpondeurs (Permettant de détecter un appareil d'intêré)
- L'ensemble des données d'appareils (Permettant d'identifier l'appariel par son nom lors du survol)

Le script passe la clé "isReadyForTraitment" de 0 au début du traitement à 1.
"""

import logging
import time
from datetime import datetime
from model.init_bdd import *
from model.init_redis import *
from model.config import *
from model.errorSquawk import *
from model.dataFlight import *
from model.sms import *

objSms = sms()
objSms.sendSMS("Start Treatment saveDB")

# On récupère la configuration
objConfig = config()
dictConfig = objConfig.getThis()

#Instanciation object Redis
objRedis = initRedis()

# On definit le path du log
logging.basicConfig(filename=objRedis.get('config_path_log').decode("utf-8") + time.strftime('%Y%m%d') + '_savebdd_adsb.log',level=logging.INFO)

#Va contenir le texte du SMS
dataTextSms = ""

#Défini si l'exécution doit continuer pour l'ensemble des scripts
objRedis.set('flagExecute_dump', 1)
objRedis.set('nameExecute_Treatment', 'DUMP')


logging.info("["+time.strftime('%d/%m/%Y %H:%M:%S').__str__()+"] ADSB-Tracking - Start DUMP.")

logging.info("["+time.strftime('%d/%m/%Y %H:%M:%S').__str__()+"] Number Flight: " + objRedis.llen('flight').__str__())
logging.info("["+time.strftime('%d/%m/%Y %H:%M:%S').__str__()+"] Current Flight: " + objRedis.llen('flight_current').__str__())
objDataFlight = dataFlight()
objDataFlight.setDataInBdd()

logging.info("["+time.strftime('%d/%m/%Y %H:%M:%S').__str__()+"] Number Squawk Error: " + objRedis.llen('squawk_error').__str__())
objErrorSquawk = errorSquawk()
objErrorSquawk.setDataInBdd()

logging.info("["+time.strftime('%d/%m/%Y %H:%M:%S').__str__()+"] ADSB-Tracking - End DUMP.")

#On repositionne le traitement
objRedis.set('flagExecute_dump', 0)
objRedis.set('nameExecute_Treatment', '')

"""
On envoie le SMS pour confirmer la bonne initialisation
"""
dataTextSms = dataTextSms+"Dump OK"

objSms.sendSMS(dataTextSms)
exit()