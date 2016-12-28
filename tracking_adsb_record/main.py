#!/usr/bin/python3.4
# -*-coding:utf8 -*

"""
Script principal. Traite l'ensemble des données de DUMP1090 pour lever les alertes
"""

import time
import requests
from datetime import datetime
from model.init_bdd import *
from model.init_redis import *
from model.config import *
from model.squawk import *
from model.dataFlight import *
from model.dataDump1090 import *
from model.sms import *

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

#Flag d'exécution de la boucle infinie, si placé à 0, on sort.
flagToExecuteLoop = 1

#Flag comptant le nombre d'itération sans traitement
objRedis.set('cpt_NoTreatment', 1)

objSms = sms()
objSms.sendSMS("Start Treatment main")

while flagToExecuteLoop:
    if objConfig.validExecuteTraitment() is True:
        if objRedis.exists('config_dump1090_host') is True :
            
            #On détruit la liste stockant les code ICAO des vols en cours.
            objDataFlight.removeAllFlightIcao()
        
            # Récupération des informations provenant de DUMP1090
            listDataFlight = objDataDump1090.getThis(objRedis.get('config_dump1090_host'))

            # On regarde si l'on a bien reçu des informations de DUMP1090, 
            # Si ce n'est pas le cas, une erreur est levée et sera présente dans "dataError"
            if listDataFlight['returnCode'] == 200:
                
                textForAlert = ''
                nbrAircraft = 0
                nbrAlert = 0
        
                # On boucle sur l'ensemble des vols capturés pour ce passage
                for key, currentFlight in enumerate(listDataFlight['dataFlight']):
                    
                    if currentFlight['flight'] != '':
                        isOkForAlert = False
                        nbrAircraft += 1
                    
                        #On stocke les code ICAO des vols en cours dans le périmètre
                        objDataFlight.addSingleFlightIcao(currentFlight['hex'])
                        
                        # Information du transpondeur pour ce vol
                        dictCurrentSquawk = objSquawk.getDataSquawkForSquawk(currentFlight['squawk'])
            
                        # Information de l'appareil pour ce vol        
                        dictCurrentAircraft = objDataFlight.getDataForRegister(currentFlight['hex'], currentFlight['flight'])
                    
                        # On regarde si le code transpondeur est militaire ou emergency
                        if dictCurrentSquawk['type'] == 1 or dictCurrentSquawk['type'] == 4:
                            isOkForAlert = True
    
                        # On regarde si le type d'appareil est militaire                     
                        if dictCurrentAircraft['isMilitary'] == 1:
                            isOkForAlert = True
                            
                        #On complète les informations du vol en cours par les informations squawk...
                        currentFlight ['squawk_type'] = dictCurrentSquawk['type']
                        currentFlight ['squawk_type_libelle'] = dictCurrentSquawk['type_libelle']
                        currentFlight ['squawk_code'] = dictCurrentSquawk['code']
                        currentFlight ['squawk_description'] = dictCurrentSquawk['description']
                        #... et type d'appareil
                        currentFlight ['aircraft_callSign'] = dictCurrentAircraft['callSign']
                        currentFlight ['aircraft_registration'] = dictCurrentAircraft['registration']
                        currentFlight ['aircraft_type'] = dictCurrentAircraft['type']
                        currentFlight ['aircraft_typeFull'] = dictCurrentAircraft['typeFull']
                        currentFlight ['aircraft_isMilitary'] = dictCurrentAircraft['isMilitary']
                        #... et la date
                        currentFlight ['date'] = datetime.now().__str__()
                        #... et la distance par rapport du point d'observation
                        currentFlight ['distance'] = 0
            
                        # Enregistrement du vol
                        objDataFlight.setDataFlight(currentFlight)
                        
                        # On construit le texte de l'alerte
                        if isOkForAlert is True and objSms.isAlertExist(currentFlight ['aircraft_callSign'], currentFlight ['squawk_code']) :
                            textForAlert = textForAlert+dictCurrentAircraft['callSign']+" "+ dictCurrentAircraft['type']+" "+dictCurrentSquawk['type_libelle']+"\r\n"
                            objSms.setAlert(currentFlight ['aircraft_callSign'], currentFlight ['squawk_code'])
                            nbrAlert += 1
                   
                
                #Si le texte de l'alerte n'est pas vide, on l'envoie
                if len(textForAlert) != 0:
                    print("["+datetime.now().__str__()+"] "+nbrAlert.__str__()+" Alert")
                    objSms.sendSMS(textForAlert)
                    
            # Si une erreur existe, c'est que nous n avons pas recupere les informations de DUMP1090
            else:
                if listDataFlight['dataError'] == 'Error Client':
                    print("["+datetime.now().__str__()+"] No connexion Dump1090: "+urlDump)
                elif listDataFlight['dataError'] == 'Error Server':
                    print("["+datetime.now().__str__()+"] Error server Dump1090: "+urlDump)
                    objSms.sendSMS("["+datetime.now().__str__()+"] Error server - End")
                    flagToExecuteLoop = 0                    
        else:
            print('Probleme de configuration')
            objSms.sendSMS("["+datetime.now().__str__()+"] Configuration Issue - End")
            flagToExecuteLoop = 0
    else:
        objRedis.incr('cpt_NoTreatment')
        print("["+datetime.now().__str__()+"] Main - Not Ready For Treatment (" + objConfig.nameExecuteTraitment() + ") ("+objRedis.get('cpt_NoTreatment').__str__()+" iterations)")
        
    #Pause de 2 secondes avant de reboucler
    time.sleep(2)
