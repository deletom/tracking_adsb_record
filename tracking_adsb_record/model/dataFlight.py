#!/usr/bin/python3.5
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
	
	def removeAllFlightIcao(self):
		self.objRedis.delete('flight_current')
		return True
		
	def addSingleFlightIcao(self, icao):
		self.objRedis.rpush('flight_current', icao)
		return True
	
	"""
	Recuparation des données de vols pour les placer dans MySQL
	"""
	def setDataInBdd(self):

		FlightCurrent = self.objRedis.lrange('flight_current', 0, -1)

		flag = True
		while flag is True:
			firstElement = self.objRedis.lindex('flight', 0)
			if firstElement is not None:
				currentFlight = json.loads(firstElement)
				self.setDataFlightinBdd(currentFlight)	
				self.objRedis.lpop('flight')
			else:
				flag = False
						
		return True
			
	def setDataFlightinBdd(self, flight):
		with self.objBdd.cursor() as cursor:
			sql = "INSERT INTO live_traffic_in_bdd(hex, squawk, flight, latitude, longitude, altitude, validposition, vert_rate, validtrack, speed, messages, seen, date, distance, type_squawk, track) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			cursor.execute(sql, (
				flight['hex']
				,flight['squawk']
				,flight['flight']
				,flight['lat']
				,flight['lon']
				,flight['altitude']
				,flight['validposition']
				,flight['vert_rate']
				,flight['validtrack']
				,flight['speed']
				,flight['messages']
				,flight['seen']
				,flight['date']
				,flight['distance']
				,flight['squawk_type']
				,flight['track']				
			))	  
			
		self.objBdd.commit()
			