#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql.cursors
import urllib
from twisted.web.client import getPage
from twisted.internet import reactor

from model.init_bdd import *
from model.config import *

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
		self.objRedis = initRedis()
		
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

	def sendSMS(self, message):
		message = urllib.quote_plus(message.encode('ascii', 'replace'))
		url = "https://smsapi.free-mobile.fr/sendmsg?user="+self.objRedis['config_sms_user']+"&pass="+self.objRedis['config_sms_pwd']+"&msg="+message
		d=getPage(url, headers={}, method="GET")
		d.addCallback(self.print_and_stop)
		d.addErrback(self.printError)
		reactor.run()
		
	def print_and_stop(self, output):
		self.dataString = output
		if reactor.running:
			reactor.stop()
						
	def printError(self, failure):
		self.dataError = str(failure)
		if reactor.running:
			reactor.stop()

		