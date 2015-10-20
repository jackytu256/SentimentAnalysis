#!/usr/bin/env python3
__author__ = 'tuhung-te'

from datetime import datetime
import time
import tweepy
import pycouchdb
import DBManager as db
import Settings as globalSettings
import Log as LogFucntions
import json

class RestfulAPI(object):

    def __init__(self,ckey,csec,atoken,asec,db_uri,loggerName):
        self.ckey = ckey;
        self.csec = csec;
        self.atoken = atoken;
        self.asec = asec;
        auth = tweepy.OAuthHandler(self.ckey,self.csec);
        auth.set_access_token(self.atoken,self.asec);
        self.auth = auth;
        self.server = pycouchdb.Server(db_uri);
        self.api = tweepy.API(self.auth)
        self.logFunctions = LogFucntions.Log(loggerName)

    def initMin_ID(self,keywords):
        while True:
            data = self.api.search(geocode=globalSettings.geoRange_Area, count=1)
            if len(data) >= 1:
                return data

    def store_Tweet_data(self,tweetData,max_id,dbmanager):
        count = 0
        list = []
        for rows in tweetData:
            row = rows._json
            max_id = min(rows.id,max_id)
            list.append(row["id_str"])
            # maybe a problem cuz the checking db function is fixed by globalSettings.db_name
            if dbmanager.isNotExisted(globalSettings.db_name,row["id_str"]):
                        dbmanager.transaction({
                            "_id": row["id_str"],
                            "user":{
                                "userName":row["user"]["name"],
                                "screen_name":row["user"]["screen_name"],
                                "followers_count":row["user"]["followers_count"],
                                "description": row["user"]["description"],
                                "statuses_count": row["user"]["statuses_count"],
                                "friends_count": row["user"]["friends_count"],
                                "listed_count": row["user"]["listed_count"]
                            },
                            "location":{
                                "coordinates": row["coordinates"]["coordinates"] if row["coordinates"] else None
                            },
                            "info":{
                                 "text": row["text"],
                                 "entities": row["entities"],
                                 "lang": row["lang"]
                            },
                            "about":{
                                "retweet_count": row["retweet_count"],
                                "source": row["source"],
                                "favorite_count": row["favorite_count"]
                            },
                            "Time":{
                                "tweet_posted_timestamp": row["created_at"],
                                "data_created_at_timestamp": time.mktime(
                                    datetime.strptime(row["created_at"], "%a %b %d %H:%M:%S +0000 %Y").timetuple())
                            }
                        },globalSettings.db_name)
                        dbmanager.transaction(row,globalSettings.db_original_Name)
            count+=1
        self.logFunctions.logger.info('insert data are :%s',str(list).strip('[]'))
        return count, max_id


    def store_Agency_data(self,tweetData,max_id,dbmanager,db_name,cDataStructure):
        count = 0
        _id = ""
        _rev = ""
        list = []
        for rows in tweetData:
            row = rows._json
            max_id = min(rows.id,max_id)
            list.append(row["id_str"])
            # maybe a problem cuz the checking db function is fixed by globalSettings.db_name
            if dbmanager.isNotExisted(db_name,row["id_str"]):
                if cDataStructure == True :
                        dbmanager.transaction({
                            "_id": row["id_str"],
                            "user":{
                                "userName":row["user"]["name"],
                                "screen_name":row["user"]["screen_name"],
                                "followers_count":row["user"]["followers_count"],
                                "description": row["user"]["description"],
                                "statuses_count": row["user"]["statuses_count"],
                                "friends_count": row["user"]["friends_count"],
                                "listed_count": row["user"]["listed_count"]
                            },
                            "location":{
                                "coordinates": row["coordinates"]["coordinates"] if row["coordinates"] else None
                            },
                            "info":{
                                 "text": row["text"],
                                 "entities": row["entities"],
                                 "lang": row["lang"]
                            },
                            "about":{
                                "retweet_count": row["retweet_count"],
                                "source": row["source"],
                                "favorite_count": row["favorite_count"]
                            },
                            "Time":{
                                "tweet_posted_timestamp": row["created_at"],
                                "data_created_at_timestamp": time.mktime(
                                    datetime.strptime(row["created_at"], "%a %b %d %H:%M:%S +0000 %Y").timetuple())
                            }
                        },db_name)
                else :
                     row["_id"] = row["id_str"]
                     dbmanager.transaction(row,db_name)
                     #_id,_rev = dbmanager.transaction(row,db_name)
                     #data = dbmanager.db[_id];
                     #data["_id"]=row["id_str"]
                     #dbmanager.transactionwithID(data,db_name)
            count+=1
        self.logFunctions.logger.info('insert data are :%s',str(list).strip('[]'))
        return count, max_id



if __name__ == '__main__':
    search_words = "Auctions OR Real Estate"
    #search_words = ['google']
    tweets_amount = 100
    restfulAPI = RestfulAPI(globalSettings.auth_keys['jacky2'].ckey,globalSettings.auth_keys['jacky2'].csec,globalSettings.auth_keys['jacky2'].atoken,globalSettings.auth_keys['jacky2'].asec,globalSettings.db_uri,"Restful")
    max_id = restfulAPI.initMin_ID(search_words)[0].id
    restfulAPI.logFunctions.logger.info('get recent ID: %s', max_id)
    count = 0
    nodata = 0
    dbmanager = db.DBManager();
    dbmanager.DBalive();
    while True:
        try:
            restfulAPI.logFunctions.logger.info('starting into while loop to get data')
            restfulAPI.logFunctions.isTimeToChangeFileName();
            data = restfulAPI.api.search(geocode=globalSettings.geoRange_Area, count=tweets_amount, result_type='recent', max_id =max_id, rpp=100)
            #data = restfulAPI.api.search(geocode=globalSettings.geoRange_Area, count=tweets_amount, result_type='recent', max_id =max_id)
            count,max_id = restfulAPI.store_Tweet_data(data,max_id,dbmanager)
            nodata = nodata+1 if count == 0 else 0
            restfulAPI.logFunctions.logger.info("current nodata is:%s", nodata)
            if nodata >=20:
                max_id = restfulAPI.initMin_ID(search_words)[0].id
                restfulAPI.logFunctions.logger.info("getting into initMin_ID because of nodata >20")
                restfulAPI.logFunctions.logger.info('get recent ID: %s', max_id)
                nodata = 0
        except tweepy.TweepError as e:
              restfulAPI.logFunctions.logger.error("Failed to get twitter data", exc_info=True)







