#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql.cursors
import json
from model.init_bdd import *
from model.init_redis import *

"""
Classe permettant de traiter les informations concernant un appareil
"""
class dataFlight:

	def __init__(self):
		self.objBdd = initBdd()
		self.objRedis = initRedis()
		self.strRegister = None
		self.strIcao = None
		
	"""
	Recuperation de l'ensemble des appareils
	Source BDD
	"""
	def findAll(self):
		with self.objBdd.cursor() as cursor:
			cursor.execute("SELECT icao, register, callsign, type_aircraft, type_aircraft_full, is_military FROM data_aircraft ORDER BY icao")
			return cursor.fetchall()
		
	"""
	Recuparation des données d'appareils pour les placer dans Redis
	"""
	def setDataInRedis(self):
		FlightAll = self.findAll()
		self.objRedis.delete('aircraft')

		# On ajoute l'ensemble des squawk à redis sous la clé "squawk"	
		for key, currentValueFlight in enumerate (FlightAll):
			self.objRedis.hset('aircraft', currentValueFlight['icao']+'_'+currentValueFlight['register'], json.dumps(currentValueFlight))		
		return self.objRedis.hlen('aircraft')
	
		
		
	"""
	On vient récupérer les informations pour un vol donné
	Source Redis
	"""
	def getDataForRegister(self, strIcao, strRegister):

		# On essaie de trouver une correcpondance d'appareil sur l'ensemble de la base que nous possédons
		if self.objRedis.hexists('aircraft', strIcao+'_'+strRegister) is True:
			currentAircraft = json.loads(self.objRedis.hget('aircraft', strIcao+'_'+strRegister))
			return {
			        'callSign':'N/A' if currentAircraft['callsign'] == '' else currentAircraft['callsign']
			        ,'registration':'N/A' if currentAircraft['register'] == '' else currentAircraft['register']
			        ,'type':'N/A' if currentAircraft['type_aircraft'] == '' else currentAircraft['type_aircraft']
			        ,'typeFull':'N/A' if currentAircraft['type_aircraft_full'] == '' else currentAircraft['type_aircraft_full']
			        ,'isMilitary':'N/A' if currentAircraft['is_military'] == '' else currentAircraft['is_military']
			}
		else:
			self.setDataAircraftForScanner(strIcao, strRegister)
			return {
				'callSign':'N/A'
				,'registration':'N/A'
				,'type':'N/A'
				,'typeFull':'N/A'
				,'isMilitary':'N/A'
	  		}

	"""
	Ajout d'un apparail dans "aircraft_error" pour le traitement ultérieur
	Source Redis
	"""
	def setDataAircraftForScanner(self, strIcao, strRegister):
		self.objRedis.rpush('aircraft_error', json.dumps([strIcao, strRegister]) )
		return True

	"""
	Enregistrement du vol en cours
	Source Redis
	"""
	def setDataFlight(self, dictCurrentFlight):
		self.objRedis.rpush('flight', json.dumps(dictCurrentFlight))
		return True
