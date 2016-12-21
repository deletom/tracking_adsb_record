#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
import pymysql.cursors
import json
from model.init_bdd import *
from model.init_redis import *

"""
Classe permettant de stocker les codes transpondeurs n'ayant pas trouvé d'équivalence dans la base Squawk
"""
class errorSquawk:

	def __init__(self):
		self.intSquawk=None
		self.objBdd = initBdd()
		self.objRedis = initRedis()
		
	# On teste
	def isExist(self, intSquawk):
		
		if self.objRedis.exists('squawk_error') is False:
			self.objRedis.set('squawk_error', '')
			return False
		else:
			listOfSquawk = json.loads(self.objRedis.get('squawk_error').decode("utf-8"))
			
			# Et on scrute la liste pour savoir si le squawk error a déjà été soulevé
			for key, currentSquawk in enumerate(listOfSquawk):
				if (currentSquawk == intSquawk):
					return True
					break
			
		return False

	# On enregistre une erreur squawk pour un traitement ultérieur
	def setSquawkForError(self, intSquawk):
		if self.isExist(intSquawk) is False:
			self.objRedis.append('squawk_error', json.dumps(intSquawk))	
		return True
