#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql.cursors
from model.config import *

"""
Classe gérant la connexion/déconnexion à la BDD
"""
class initBdd(object):

	__instance = None

	def __new__(cls):
		if initBdd.__instance is None:
			initBdd.__instance = object.__new__(cls)
			
		objConfig = config()
		dictConfig = objConfig.getThis()			
			
		initBdd.__instance = pymysql.connect(user=dictConfig['bdd']['user'], password=dictConfig['bdd']['pwd'], host=dictConfig['bdd']['host'], db=dictConfig['bdd']['database'], charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
		return initBdd.__instance
		
	def closeBdd(self):
		initBdd.__instance.close()
