#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
from model.config import *

"""
Récupération des données provenant de DUMP1090
"""
class dataDump1090():
    
        dataString = None
        dataError = None
        returnCode = 200

        def getThis(self, urlDump):
            returnRequest = requests.get(urlDump)
            returnCode = returnRequest.status_code
            
            if returnCode >= 400 and returnCode < 500:
                dataError = 'Error Client'
                self.returnCode = returnCode 
            if returnCode >= 500 and returnCode < 600:
                dataError = 'Error Server'
                self.returnCode = returnCode
            if returnCode == 200:
                self.dataString = returnRequest.json()

            return {
                'dataFlight':self.dataString
                ,'dataError':self.dataError
                ,'returnCode':self.returnCode
            }
