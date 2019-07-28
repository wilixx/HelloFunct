# coding=utf-8
'''
Created on 2019 年07月21日

@author: Allen Guo
'''
import configparser
import os

configdir = os.getcwd()
configPath = configdir + "\\config\\config.properties"


class config(object):
    def __init__(self):
        pass

    def getConfig(self, tag, valueList):
        returnVal = []
        cf = configparser.ConfigParser()
        cf.read(configPath)
        for value in valueList:
            returnVal.append(cf.get(tag, value))
        return returnVal

    def getSigleConfig(self, tag, value):
        cf = configparser.ConfigParser()
        cf.read(configPath)
        return cf.get(tag, value)