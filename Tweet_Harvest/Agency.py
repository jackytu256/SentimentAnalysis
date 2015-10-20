#!/usr/bin/env python3
__author__ = 'tuhung-te'


import tweepy
import pycouchdb
import DBManager as db
import Settings as globalSettings
import Log as LogFucntions
from Restful import RestfulAPI




if __name__ == '__main__':
    tweets_amount = 100
    restfulAPI = RestfulAPI(globalSettings.auth_keys['zoey'].ckey,globalSettings.auth_keys['zoey'].csec,globalSettings.auth_keys['zoey'].atoken,globalSettings.auth_keys['zoey'].asec,globalSettings.db_uri,"Agency")
    count = 0
    nodata = 0
    dbmanager = db.DBManager();
    dbmanager.DBalive();
    while True:
        try:
            restfulAPI.logFunctions.logger.info("getting into loop to search user data")
            for row in globalSettings.search_users:
                if row['max_id'] == 0:
                   data  = restfulAPI.api.user_timeline(id=row['User_ID'],count=1,resut_type='recent')
                   row['max_id'] = data[0].id
                else :
                   data = restfulAPI.api.user_timeline(id=row['User_ID'],count= tweets_amount,max_id=row['max_id'])
                   row['count'],row['max_id'] = restfulAPI.store_Agency_data(data,row['max_id'],dbmanager,globalSettings.db_follow_name,True)
                   restfulAPI.store_Agency_data(data,0,dbmanager,globalSettings.db_original_follow_Name,False)
                   row['nodata'] =  row['nodata']+1 if row['count'] == 0 else 0
                   restfulAPI.logFunctions.logger.info("current nodata is:%s", nodata)
                   if nodata >=20:
                        data  = restfulAPI.api.user_timeline(id=row['User_ID'],count=1,resut_type='recent')
                        row['max_id'] = data[0].id
                        restfulAPI.logFunctions.logger.info("getting new max_id because of nodata >20")
                        restfulAPI.logFunctions.logger.info('get recent ID: %s',  row['max_id'])
                        nodata = 0
        except tweepy.TweepError as e:
              restfulAPI.logFunctions.logger.error("Failed to get twitter data", exc_info=True)