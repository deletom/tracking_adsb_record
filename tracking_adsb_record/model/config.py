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
		
		# Si la clé "config_adsb" n'existe pas
		if objRedis.exists('config_adsb') is False:
			# On récupère les informations dans le fichier
			with open('./config.json', 'r') as fs:
				contentJson = json.loads(fs.read())
				fs.close()
				
				# Et on ajoute le contenu dans la "config_adsb" de Redis
				# La clé "config_adsb" expire au bout de 30 minutes 
				objRedis.set('config_adsb', json.dumps(contentJson), 1800)
				
				# Et on renvoie la config
				return contentJson

		# Si la clé "config_adsb" existe dans Redis			
		else:
			return json.loads(objRedis.get('config_adsb'))
