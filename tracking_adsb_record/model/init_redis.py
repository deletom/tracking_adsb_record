#!/usr/bin/env python
# -*- coding: utf-8 -*-
import redis
from model.config import *

"""
Classe gérant la connexion à Redis
"""
class initRedis(object):

	__instance = None

	def __new__(cls):
		if initRedis.__instance is None:
			initRedis.__instance = object.__new__(cls)
			
		objConfig = config()
		dictConfig = objConfig.getThis()			
			
		initRedis.__instance = redis.StrictRedis(host=dictConfig['redis']['host'], port=dictConfig['redis']['port'], db=0)
		return initRedis.__instance
