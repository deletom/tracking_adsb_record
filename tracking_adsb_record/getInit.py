#!/usr/bin/env python
# -*-coding:utf8 -*
from datetime import datetime
from model.init_bdd import *
from model.init_redis import *
from model.init import *
from model.config import *
from model.squawk import *
from model.dataFlight import *
from model.dataDump1090 import *

objRedis = initRedis()

print("["+datetime.now().__str__()+"] ADSB-Tracking - Debut de l initialisation")
"""
On instancie l'objet gérant les configurations
Et on récupère les informations pour les placer dans Redis
Clé : config_*
"""
print("["+datetime.now().__str__()+"] ADSB-Tracking - Recuperation de la configuration")
objConfig = config()
objConfig.getThis()

"""
On instancie l'objet gérant les squawk
Et on récupère les informations pour les placer dans Redis
Clé : squawk
"""
print("["+datetime.now().__str__()+"] ADSB-Tracking - Recuperation des squawk")
objSquawk = squawk()
objSquawk.setDataInRedis()

"""
On instancie l'objet gérant les données d'appareils
Et on récupère les informations pour les placer dans Redis
Clé : aircraft
"""
print("["+datetime.now().__str__()+"] ADSB-Tracking - Recuperation des donnees d appareil")
objDataFlight = dataFlight()
objDataFlight.setDataInRedis()

print("["+datetime.now().__str__()+"] ADSB-Tracking - Fin de l initialisation")