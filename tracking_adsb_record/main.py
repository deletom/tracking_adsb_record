#!/usr/bin/env python
# -*-coding:utf8 -*
from model.init_bdd import *
from model.squawk import *
from model.config import *
from model.dataDump1090 import *
from model.dataFlight import *

# Instanciation des différents objets
objSquawk = squawk()
objDataDump1090 = dataDump1090()
objDataFlight = dataFlight()

objConfig = config()
dictConfig = objConfig.getThis()  
urlDump = dictConfig['dump1090']['host']   

# On va boucler indéfiniment
while(1):
    
    # Récupération des informations provenant de DUMP1090
    listDataFlight = objDataDump1090.getThis(urlDump.encode('ascii', 'replace'))
    
    print(listDataFlight)

    """
    # On boucle sur l'ensemble des vols capturés pour ce passage
    for key, currentFlight in enumerate(listDataFlight):
        
        # Information du transpondeur pour ce vol
        dictCurrentSquawk = objSquawk.getDataSquawkForSquawk(currentFlight['squawk'])

        # Information de l'appareil pour ce vol        
        dictCurrentAircraft = objDataFlight.getDataForRegister(currentFlight['hex'], currentFlight['flight'])



        # Enregistrement du vol
        objDataFlight.setDataFlight(currentFlight)
    """ 
        
        
    exit()