#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
import redis

"""
Classe gérant la connexion à Redis
"""
class initRedis(object):

	__instance = None

	def __new__(cls):
		if initRedis.__instance is None:
			initRedis.__instance = object.__new__(cls)	
			
		initRedis.__instance = redis.StrictRedis(host="localhost", port="6379", db=0)
		return initRedis.__instance
	
	def flushall(self):
		initRedis.__instance.flushall()
