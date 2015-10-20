__author__ = 'tuhung-te'
import csv

class DataLoader(object):
    def __init__(self):
        self.a = "a"


    def loadCSV(self,fileName):
        resource = open(fileName,'r')
        reader = csv.DictReader(resource,delimiter=',')
        return reader