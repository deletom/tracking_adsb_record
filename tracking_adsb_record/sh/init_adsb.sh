#!/bin/bash

# Informations pour les logs
LOG_PATH=[PATH LOG]
DATE=$(date +"%Y%m%d")
LOGFILE=${LOG_PATH}${DATE}_adsb.txt

# Informations pour Python
PYTHON_PATH=[PATH PYTHON]
PYTHON_VERSION=3.4

echo "$(date +"%d/%m/%Y %H:%M:%S") Lancement du systeme ADSB" | tee -a ${LOGFILE}


# On se place dans le dossier d'execution de python
echo "$(date +"%d/%m/%Y %H:%M:%S") Placement dans le dossier ${PYTHON_PATH}" | tee -a ${LOGFILE}
cd $PYTHON_PATH



# Nettoyage du serveur Redis
echo "$(date +"%d/%m/%Y %H:%M:%S") Nettoyage du serveur Redis" | tee -a ${LOGFILE}
python${PYTHON_VERSION} resetRedis.py | tee -a ${LOGFILE}



# On lance l'initialisation du systeme de tracking ADSB
echo "$(date +"%d/%m/%Y %H:%M:%S") Initialisation du systeme, importation des donnees dans Redis" | tee -a ${LOGFILE}
python${PYTHON_VERSION} getInit.py | tee -a ${LOGFILE}



# On lance le script principal du systeme de tracking ADSB
echo "$(date +"%d/%m/%Y %H:%M:%S") Lancement du systeme de tracking ADSB" | tee -a ${LOGFILE}
python${PYTHON_VERSION} main.py | tee -a ${LOGFILE}

exit 0
