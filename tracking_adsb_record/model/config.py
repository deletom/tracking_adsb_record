#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql.cursors
import json

from model.init_bdd import *

"""
Classe permettant de récupérer les informations de configuration en fichier.
"""
class config():

	def getThis(cls):
		with open('./config.json', 'r') as fs:
			contentJson = json.loads(fs.read())
			fs.close()
			return contentJson
		

