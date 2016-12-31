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
import time
import logging
from datetime import datetime
from model.init_bdd import *
from model.init_redis import *
from model.config import *
from model.squawk import *
from model.dataFlight import *
from model.dataDump1090 import *
from model.sms import *

#Instanciation object sms
objSms = sms()

#Instanciation object Redis
objRedis = initRedis()

#Va contenir le texte du SMS
dataTextSms = ""

#Défini si l'exécution doit continuer pour l'ensemble des scripts
objRedis.set('flagExecute_Treatment', 0)
objRedis.set('nameExecute_Treatment', 'INIT')

"""
On instancie l'objet gérant les configurations
Et on récupère les informations pour les placer dans Redis
Clé : config_*
"""
objConfig = config()
objConfig.getThis()
dataTextSms = dataTextSms+"Config OK \r\n"

# On definit le path du log
logging.basicConfig(filename=objRedis.get('config_path_log')+time.strftime('%Y%m%d').__str__()+'_adsb.log',level=logging.DEBUG)

"""
On instancie l'objet gérant les squawk
Et on récupère les informations pour les placer dans Redis
Clé : squawk
"""
objSquawk = squawk()
returnSquawk = objSquawk.setDataInRedis()
dataTextSms = dataTextSms+" "+returnSquawk.__str__()+" Squawk \r\n"

"""
On instancie l'objet gérant les données d'appareils
Et on récupère les informations pour les placer dans Redis
Clé : aircraft
"""
objDataFlight = dataFlight()
returnAircraft = objDataFlight.setDataInRedis()
dataTextSms = dataTextSms+" "+returnAircraft.__str__()+" Aircraft \r\n"

logging.info("["+datetime.now().__str__()+"] ADSB-Tracking - Squawk OK ("+returnSquawk.__str__()+")")
logging.info("["+datetime.now().__str__()+"] ADSB-Tracking - Aircraft OK ("+returnAircraft.__str__()+")")

if int(returnSquawk.__str__()) != 0 and int(returnAircraft.__str__()) != 0:   
    objRedis.set('flagExecute_Treatment', 1)
    objRedis.set('nameExecute_Treatment', '')
    
if objRedis.get('flagExecute_Treatment').decode("utf-8") == '1':
    logging.info("["+datetime.now().__str__()+"] ADSB-Tracking - OK Treatment.")
    dataTextSms = dataTextSms+" OK for Treatment \r\n"
else:
    logging.info("["+datetime.now().__str__()+"] ADSB-Tracking - KO Treatment.")
    dataTextSms = dataTextSms+" KO for Treatment \r\n"   
    
logging.info("["+datetime.now().__str__()+"] ADSB-Tracking - End INIT.")

"""
On envoie le SMS pour confirmer la bonne initialisation
"""
objSms.sendSMS(dataTextSms)
exit()