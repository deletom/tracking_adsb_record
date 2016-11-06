#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql.cursors
import json

from model.init_redis import *

"""
Classe permettant de récupérer les informations de configuration 
dans le fichier config.json à la racine du projet.

On stocke le contenu de la configuration sous redis (clé:config_adsb)
A chaque itération, la configuration ne sera pas récupérée dans le fichier mais en RAM
"""
class config():
	
	contentJson = None

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

			return True
