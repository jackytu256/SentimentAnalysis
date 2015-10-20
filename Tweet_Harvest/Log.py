__author__ = 'tuhung-te'
import logging
from datetime import datetime
import time


class Log(object):
    def __init__(self,fileName):
        self.timeForFile = datetime.today().timetuple().tm_yday
        self.prefix = fileName
        self.fileName = str.format("{}-{}.log",self.prefix,datetime.now().strftime('%Y-%m-%d'))
        logging.basicConfig(filename= self.fileName,level=logging.INFO)
        self.logger = logging.getLogger()



    def changeFileName(self):
        fhandler =logging.FileHandler(self.fileName)
        formatter = logging.Formatter("%(asctime)s %(filename)s, %(lineno)d, %(funcName)s: %(message)s")
        fhandler.setFormatter(formatter)
        for handler in self.logger.handlers:
            self.logger.removeHandler(handler)

        self.logger.addHandler(fhandler)

    def isTimeToChangeFileName(self):
        currentDayOfYear = datetime.today().timetuple().tm_yday
        #self.timeForFile = 227
        if currentDayOfYear > self.timeForFile :
            self.fileName = str.format("{}-{}.log",self.prefix,datetime.now().strftime('%Y-%m-%d'))
            self.timeForFile = currentDayOfYear
            self.changeFileName()


