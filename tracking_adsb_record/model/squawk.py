#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql.cursors
import json
from model.init_bdd import *
from model.init_redis import *
from model.errorSquawk import *

"""
Classe permettant de récupérer les informations de squawk (Code transpondeur) et de déterminer 
les informations du code transpondeur suivant le vol que l'on est entrain de traiter

Les informations de code transpondeur (Squawk) sont stockées en base de données et sont éditables
via l'interface web.

En BDD nous avons :
Une borne inférieure et une borne supérieure, les codes transpondeurs peuvent définis soit pour 
un chiffre exact soit pour une plage
Un type, Militaire/Civil
Et une description symbolisant les informations que renvoient ce code.
"""
class squawk:

	def __init__(self):
		self.objRedis = initRedis()
		self.objBdd = initBdd()
		self.dictTypeOfSquawk={
		        '1':'military'
		        ,'2':'civil'
		        ,'3':'mixte'
		        ,'4':'emergency'
		}
		
	"""
	Recuperation de l'ensemble des squawk en BDD
	"""
	def findAll(self):
		with self.objBdd.cursor() as cursor:
			
			cursor.execute("SELECT borne_inf, borne_sup, type, description FROM squawk ORDER BY borne_inf");
			
			return	cursor.fetchall()
			
	"""
	Permet d ajouter l ensemble des squawk de la BDD à Redis
	"""
	def setDataInRedis(self):
		squawkAll = self.findAll()
		self.objRedis.delete('squawk')

		# On ajoute l'ensemble des squawk à redis sous la clé "squawk"	
		for key, currentValueSquawk in enumerate (squawkAll):
			self.objRedis.lpush('squawk', json.dumps(currentValueSquawk))		
		return self.objRedis.llen('squawk')
	
	
	

	# Determination du type de squawk suivant un identifiant transpondeur
	def getDataSquawkForSquawk(self, intSquawk):	
			
		numberElement = self.objRedis.llen('squawk')
		
		index = 0	
			
		while index < numberElement:
			currentSquawk = json.loads(self.objRedis.lindex('squawk', index))
			if currentSquawk['borne_sup'] == "":
				if intSquawk == currentSquawk['borne_inf']:
					return {
					        'type':currentSquawk['type']
					        ,'type_libelle':self.dictTypeOfSquawk[currentSquawk['type']]
					        ,'code':intSquawk
					        ,'description':currentSquawk['description']
					}
			elif intSquawk >= currentSquawk['borne_inf'] and intSquawk <= currentSquawk['borne_sup']:
				return {
			                'type':currentSquawk['type']
			                ,'type_libelle':self.dictTypeOfSquawk[currentSquawk['type']]
			                ,'code':intSquawk
			                ,'description':currentSquawk['description']
			        }
			index += 1
			
		#Si rien n'a été trouvé pour ce code, on l'ajoute à la liste des codes en erreur pour une recherche futur
		#objErrorSquawk = errorSquawk()
		#objErrorSquawk.setSquawkForError(intSquawk)
		return {
                        'type':0
                        ,'type_libelle':'N/A'
                        ,'code':intSquawk
                        ,'description':'N/A'
                }

