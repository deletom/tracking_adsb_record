#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql.cursors
from model.init_bdd import *

"""
Classe permettant de stocker les codes transpondeurs n'ayant pas trouvé d'équivalence dans la base Squawk
"""
class errorSquawk:

	def __init__(self):
		self.intSquawk=None
		self.objBdd = initBdd()
		
	# Recuperation de l'ensemble des squawks en base
	def isExist(self, intSquawk):
		with self.objBdd.cursor() as cursor:
			cursor.execute("SELECT code_squawk FROM squawk_error WHERE code_squawk=%s", intSquawk)
			if len(cursor.fetchall()) == 0:
				return True
			return False

	# On enregistre une erreur squawk pour un traitement ultérieur
	def setSquawkForError(self, intSquawk):
		with self.objBdd.cursor() as cursor:
			if self.isExist(intSquawk) is False:
				cursor.execute("INSERT INTO squawk_error (code_squawk) VALUES (%s)", (intSquawk))
				self.objBdd.commit()			
		return True
