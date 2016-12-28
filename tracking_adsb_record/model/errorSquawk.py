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
		self.intInsertMultiple = 1
		self.sql = ""

	# On enregistre une erreur squawk pour un traitement ultérieur
	def setSquawkForError(self, intSquawk):
		SquawkErrorCurrent = self.objRedis.lrange('squawk_error', 0, -1)
		if intSquawk not in SquawkErrorCurrent:
			self.objRedis.rpush('squawk_error', intSquawk)
		return True
	
	"""
	Recuparation des données de vols pour les placer dans MySQL
	"""
	def setDataInBdd(self):

		flag = True
		while flag is True:
			firstElement = self.objRedis.lindex('squawk_error', 0)
			if firstElement is not None:
				currentSquawk = firstElement.decode("utf-8")
				self.setDataSquawkinBdd(currentSquawk)	
				self.objRedis.lpop('squawk_error')
			else:
				flag = False
		self.objBdd.commit()	  
				
		return True
			
	def setDataSquawkinBdd(self, squawk):
		with self.objBdd.cursor() as cursor:

			if self.intInsertMultiple == 1:
				self.sql = "INSERT INTO squawk_error(code_squawk) VALUES "

			if self.intInsertMultiple == 1:
				self.sql += "('%s')" % (squawk)
			else:
				self.sql += ", ('%s')" % (squawk)
		  	
			self.intInsertMultiple += 1

			if self.intInsertMultiple == 20:
				cursor.execute(self.sql)
				self.intInsertMultiple = 1
