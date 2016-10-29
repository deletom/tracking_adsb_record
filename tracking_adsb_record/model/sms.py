#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql.cursors
from model.init_bdd import *

"""
Classe permettant de traiter les informations concernant un appareil
"""
class sms:

	def __init__(self):
		self.objBdd = initBdd()
		self.strIcao = None
		self.strFlight = None
		self.intSquawk = None
		self.intType = None
		
	# Envoi de l'alerte
	def setAlert(self, strIcao, strFlight, intSquawk, intType):
		self.strIcao = strIcao
		self.strFlight = strFlight
		self.intSquawk = intSquawk
		self.intType = intType
		with self.objBdd.cursor() as cursor:
			cursor.execute("SELECT id FROM alerte_sms WHERE flight=%s AND date=NOW()", (self.strFlight));
			rows = cursor.fetchall()
			
			if len(rows)==0:
				cursor.execute("INSERT INTO alerte_sms (date, flight, squawk, type_squawk, send) VALUES (NOW(), %s, %s, %s, 0)", (self.strFlight, self.intSquawk, self.intType))
				self.objBdd.commit()	
			return True
