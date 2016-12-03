#!/usr/bin/env python
# -*-coding:utf8 -*

"""
Script d'initialisation des éléments Redis permettant le fonctionnement du script "main.py"
3 phases principales
- Récupération des éléments de configuration (BDD, Redis, URL Dump1090)
- L'ensemble des codes transpondeurs (Permettant de détecter un appareil d'intêré)
- L'ensemble des données d'appareils (Permettant d'identifier l'appariel par son nom lors du survol)

Le script passe la clé "isReadyForTraitment" de 0 au début du traitement à 1.
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