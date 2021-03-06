#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
import pymysql.cursors
import urllib3
import requests
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
		return self.objRedis.hexists('alert', strIcao+'_'+intSquawk)

	def sendSMS(self, message):
		url = "https://smsapi.free-mobile.fr/sendmsg"	
		parameter = {'user': self.objRedis['config_sms_user'], 'pass': self.objRedis['config_sms_pwd'], 'msg': message}
		
		urllib3.disable_warnings()
		
		returnRequest = requests.get(url, params=parameter, verify=False)
				
		returnCode = returnRequest.status_code
		
		if returnCode >= 400 and returnCode < 500:
			dataReturn = 'Error Client'
			self.returnCode = returnCode 
		if returnCode >= 500 and returnCode < 600:
			dataReturn = 'Error Server'
		if returnCode == 200:
			dataReturn = 'OK'

		return {
			'dataReturn':dataReturn
			,'returnCode':returnCode
		}
