#!/usr/bin/env python
# -*-coding:utf8 -*
from model.init_bdd import *
from model.init_redis import *
from model.init import *
from model.config import *
from model.squawk import *
from model.dataFlight import *
from model.dataDump1090 import *

# On instancie l'objet Redis
objRedis = initRedis()

# On récupère la configuration
objConfig = config()
dictConfig = objConfig.getThis()

# On instancie l'objet nous permettant de récupérer les informations des appareils
objDataDump1090 = dataDump1090()

# On instancie l'objet gérant les squawk
objSquawk = squawk()

# On instancie l'objet gérant les données d'appareil
objDataFlight = dataFlight()

while 1:   
    # URL du système DUMP1090
    urlDump = dictConfig['dump1090']['host'].encode('ascii', 'replace')
    
    # Récupération des informations provenant de DUMP1090
    listDataFlight = objDataDump1090.getThis(urlDump)
    
    # On regarde si l'on a bien reçu des informations de DUMP1090, 
    # Si ce n'est pas le cas, une erreur est levée et sera présente dans "dataError"
    if listDataFlight['dataError'] is None:

        # On boucle sur l'ensemble des vols capturés pour ce passage
        for key, currentFlight in enumerate(listDataFlight['dataFlight']):
            
            # Information du transpondeur pour ce vol
            dictCurrentSquawk = objSquawk.getDataSquawkForSquawk(currentFlight['squawk'])
    
            # Information de l'appareil pour ce vol        
            dictCurrentAircraft = objDataFlight.getDataForRegister(currentFlight['hex'], currentFlight['flight'])

            # Enregistrement du vol
            objDataFlight.setDataFlight(currentFlight)
            
    # Dans le cas où l'erreur serait présente on l'affiche 
    else:
        print('Pas de connexion: '+urlDump)
        
    exit()
   
