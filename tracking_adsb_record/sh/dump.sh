#!/bin/bash

# Informations pour les logs
LOG_PATH=[PATH LOG]
DATE=$(date +"%Y%m%d")
LOGFILE=${LOG_PATH}${DATE}_adsb.txt

# Informations pour Python
PYTHON_PATH=[PATH PYTHON]
PYTHON_VERSION=3.4

echo "$(date +"%d/%m/%Y %H:%M:%S") Lancement du systeme ADSB" | tee -a ${LOGFILE}

echo "$(date +"%d/%m/%Y %H:%M:%S") Placement dans le dossier ${PYTHON_PATH}" | tee -a ${LOGFILE}
cd $PYTHON_PATH



# On lance le diagnostic
echo "$(date +"%d/%m/%Y %H:%M:%S") Lancement du diagnostic" | tee -a ${LOGFILE}
python${PYTHON_VERSION} diagnostic.py | tee -a ${LOGFILE}



# On lance l'initialisation du systeme de tracking ADSB
echo "$(date +"%d/%m/%Y %H:%M:%S") Dump des donnees Redis sous MySQL" | tee -a ${LOGFILE}
python${PYTHON_VERSION} saveDataInBdd.py | tee -a ${LOGFILE}



# On lance le diagnostic
echo "$(date +"%d/%m/%Y %H:%M:%S") Lancement du diagnostic" | tee -a ${LOGFILE}
python${PYTHON_VERSION} diagnostic.py | tee -a ${LOGFILE}


exit 0
