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
		self.objRedis = initRedis()
		
	# On stocke les alertes déjà envoyées
	def setAlert(self, strIcao, intSquawk):
		self.objRedis.hset('alert', strIcao+'_'+intSquawk, 'send')
		return True
		
	# L'alerte a-t-elle déjà été envoyées aujourd'hui ?
	def isAlertExist(self, strIcao, intSquawk):
		return self.objRedis.hexists('alert', self.strIcao+'_'+self.intSquawk)

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

		