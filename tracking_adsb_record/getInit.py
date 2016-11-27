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
from model.init_bdd import *
from model.init_redis import *
from model.init import *
from model.config import *
from model.squawk import *
from model.dataFlight import *
from model.dataDump1090 import *
from model.sms import *

#Instanciation object Redis
objRedis = initRedis()

#Va contenir le texte du SMS
dataTextSms = ""

#Défini si l'exécution doit continuer pour l'ensemble des scripts
objRedis.set('isReadyForTraitment', 0)


print("["+datetime.now().__str__()+"] ADSB-Tracking - Debut INIT.")

"""
On instancie l'objet gérant les configurations
Et on récupère les informations pour les placer dans Redis
Clé : config_*
"""
print("["+datetime.now().__str__()+"] ADSB-Tracking - Config")
objConfig = config()
objConfig.getThis()
dataTextSms = dataTextSms+"Config OK \r\n"

"""
On instancie l'objet gérant les squawk
Et on récupère les informations pour les placer dans Redis
Clé : squawk
"""
print("["+datetime.now().__str__()+"] ADSB-Tracking - Squawk")
objSquawk = squawk()
returnSquawk = objSquawk.setDataInRedis()
dataTextSms = dataTextSms+" "+returnSquawk.__str__()+" Squawk \r\n"
print("["+datetime.now().__str__()+"] ADSB-Tracking - Squawk OK ("+returnSquawk.__str__()+")")

"""
On instancie l'objet gérant les données d'appareils
Et on récupère les informations pour les placer dans Redis
Clé : aircraft
"""
print("["+datetime.now().__str__()+"] ADSB-Tracking - Aircraft")
objDataFlight = dataFlight()
returnAircraft = objDataFlight.setDataInRedis()
dataTextSms = dataTextSms+" "+returnAircraft.__str__()+" Aircraft \r\n"
print("["+datetime.now().__str__()+"] ADSB-Tracking - Aircraft OK ("+returnAircraft.__str__()+")")

if int(returnSquawk.__str__()) != 0 and int(returnAircraft.__str__()) != 0:   
    objRedis.set('isReadyForTraitment', 1)
    
if objRedis.get('isReadyForTraitment') == '1':
    print("["+datetime.now().__str__()+"] ADSB-Tracking - OK pour traitement.")
    dataTextSms = dataTextSms+" OK for Traitment \r\n"
else:
    print("["+datetime.now().__str__()+"] ADSB-Tracking - KO pour traitement.")
    dataTextSms = dataTextSms+" KO for Traitment \r\n"   
    
print("["+datetime.now().__str__()+"] ADSB-Tracking - Fin INIT.")

"""
On envoie le SMS pour confirmer la bonne initialisation
"""
objSms = sms()
#objSms.sendSMS(dataTextSms)
exit()