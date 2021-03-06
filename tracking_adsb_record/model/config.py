#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
import pymysql.cursors
import json

from model.init_redis import *

"""
Classe généraliste gérant la configuration et certains éléments d'exécution
"""
class config():
	
	contentJson = None

	"""
	Méthode permettant de récupérer les informations de configuration 
	dans le fichier config.json à la racine du projet.
	
	On stocke le contenu de la configuration sous redis (clé:config_adsb)
	"""
	def getThis(cls):
		# On initialise Redis
		objRedis = initRedis()

		# On récupère les informations dans le fichier
		with open('./config.json', 'r') as fs:
			contentJson = json.loads(fs.read())
			fs.close()

			#On vient stocker les élements de configuration sous Redis
			objRedis.set('config_dump1090_host', contentJson['dump1090']['host'].encode('ascii', 'replace'))
			
			objRedis.set('config_bdd_host', contentJson['bdd']['host'])
			objRedis.set('config_bdd_user', contentJson['bdd']['user'])
			objRedis.set('config_bdd_pwd', contentJson['bdd']['pwd'])
			objRedis.set('config_bdd_database', contentJson['bdd']['database'])
			
			objRedis.set('config_sms_user', contentJson['sms_free']['user'])
			objRedis.set('config_sms_pwd', contentJson['sms_free']['pwd'])
			
			objRedis.set('config_path_log', contentJson['path']['log'].encode('ascii', 'replace'))

			return True

	"""
	Méthode permettant de définir si, lors de cette itération, l'exécution de l'ensemble des traitements
	peut bien s'effectuer.
	"""		
	def validExecuteTraitment(self):
		objRedis = initRedis()

		# Flag positionne a l'initialisation
		if objRedis.get('flagExecute_Treatment').decode("utf-8") == '0':
			return False
		# Flag positionne a l'initialisation mais pilotable depuis l'IHM pour stopper le traitement
		if objRedis.get('flagExecute_Treatment_Force').decode("utf-8") == '0':
			return False
		# Flag positionne a l'initialisation mais modifie par le dump pour stopper le traitement.
		if objRedis.exists('flagExecute_dump') is True:
			if objRedis.get('flagExecute_dump').decode("utf-8") == '1':
				return False
		
		return True

	"""
	Renvoi le nom du script ayant bloqué le traitement
	"""		
	def nameExecuteTraitment(self):
		objRedis = initRedis()
		return objRedis.get('nameExecute_Treatment').decode("utf-8")