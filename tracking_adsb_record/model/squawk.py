#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql.cursors
from model.init_bdd import *
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
		self.listSquawk=[]
		self.dictTypeOfSquawk={
		        1:'military'
		        ,2:'civil'
		        ,3:'mixte'
		        ,4:'emergency'
		}
		
	# Recuperation de l'ensemble des squawks en base
	def findAll(self):
		objBdd = initBdd()
		with objBdd.cursor() as cursor:
			cursor.execute("SELECT borne_inf, borne_sup, type, description FROM squawk ORDER BY borne_inf");
			rows = cursor.fetchall()
			for row in rows:
				self.listSquawk.append(row)
			return self.listSquawk

	# Determination du type de squawk suivant un identifiant transpondeur
	def getDataSquawkForSquawk(self, intSquawk):
		# Si nous n'avons pas encore rempli la liste des squawks <listSquawk> nous recherchons l'ensemble en BDD
		if len(self.listSquawk) == 0:
			self.findAll()		
			
		# Et on scrute la liste pour trouver le bon squawk
		for key, currentSquawk in enumerate(self.listSquawk):
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

		#Si rien n'a été trouvé pour ce code, on l'ajoute à la liste des codes en erreur pour une recherche futur
		objErrorSquawk = errorSquawk()
		objErrorSquawk.setSquawkForError(intSquawk)
		return {
                        'type':0
                        ,'type_libelle':'N/A'
                        ,'code':intSquawk
                        ,'description':'N/A'
                }
