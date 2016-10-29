#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from twisted.web.client import getPage
from twisted.internet import reactor
from model.config import *

"""
Récupération des données provenant de DUMP1090
"""
class dataDump1090():
        
        dataString = None

        def print_and_stop(self, output):
                self.dataString = output
                if reactor.running:
                        reactor.stop()

        def getThis(self, urlDump):
                objConfig = config()
                dictConfig = objConfig.getThis()                
                d = getPage(urlDump)
                d.addCallback(self.print_and_stop)
                reactor.run()
                return json.loads(self.dataString)
                

"""
{u'squawk': u'1000', u'flight': u'CND9112 ', u'messages': 305, u'track': 37, u'lon': 2.453737, 
u'altitude': 38000, u'vert_rate': -64, u'hex': u'484f2e', u'validposition': 1, u'validtrack': 1, 
u'lat': 49.93058, u'seen': 0, u'speed': 431}
"""