#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql.cursors
from model.init_bdd import *

"""
Classe permettant de traiter les informations concernant un appareil
"""
class dataFlight:

	def __init__(self):
		self.objBdd = initBdd()
		self.strRegister = None
		self.strIcao = None
		
	# On vient récupérer les informations pour un vol donné, si les informations n'existent pas, on renvoi false
	def getDataForRegister(self, strIcao, strRegister):
		self.strIcao = strIcao
		self.strRegister = strRegister

		with self.objBdd.cursor() as cursor:
			cursor.execute("SELECT icao, register, callsign, type_aircraft, type_aircraft_full, is_military FROM data_aircraft WHERE icao=%s", self.strIcao)
			rows = cursor.fetchall()
			if len(rows) == 1:
				return {
				        'callSign':'N/A' if rows[0]['callsign'] == '' else rows[0]['callsign']
				        ,'registration':'N/A' if rows[0]['register'] == '' else rows[0]['register']
				        ,'type':'N/A' if rows[0]['type_aircraft'] == '' else rows[0]['type_aircraft']
				        ,'typeFull':'N/A' if rows[0]['type_aircraft_full'] == '' else rows[0]['type_aircraft_full']
				        ,'isMilitary':'N/A' if rows[0]['is_military'] == '' else rows[0]['is_military']
				}
			else:
				self.setDataAircraftForScanner()
			return {
				'callSign':'N/A'
				,'registration':'N/A'
				,'type':'N/A'
				,'typeFull':'N/A'
				,'isMilitary':'N/A'
	  		}
	
	def setDataAircraftForScanner(self):
		with self.objBdd.cursor() as cursor:
			cursor.execute("INSERT INTO data_aircraft (icao, register) VALUES (%s, %s)", (self.strIcao, self.strRegister))
			self.objBdd.commit()	
			return True
		

	def setDataFlight(self, dictCurrentFlight):
		with self.objBdd.cursor() as cursor:
			#currentFlight
			cursor.execute("INSERT INTO live_traffic_in_bdd (hex, squawk, flight, latitude, longitude, altitude, validposition, vert_rate, validtrack, speed, messages, seen, date, distance, type_squawk, track) VALUES (%s)", currentFlight)
			self.objBdd.commit()				