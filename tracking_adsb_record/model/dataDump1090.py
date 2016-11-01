#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from twisted.web.client import getPage
from twisted.internet import reactor
from twisted.python.log import err
from model.config import *

"""
Récupération des données provenant de DUMP1090
"""
class dataDump1090():
        
        dataString = None
        dataError = None

        def print_and_stop(self, output):
                self.dataString = json.loads(output)
                if reactor.running:
                    reactor.stop()
                        
        def printError(self, failure):
            self.dataError = str(failure)
            if reactor.running:
                reactor.stop()


        def getThis(self, urlDump):
                objConfig = config()
                dictConfig = objConfig.getThis()                
                d = getPage(urlDump)
                d.addCallback(self.print_and_stop)
                d.addErrback(self.printError)
                reactor.run()

                return {
                    'dataFlight':self.dataString
                    ,'dataError':self.dataError
                }
