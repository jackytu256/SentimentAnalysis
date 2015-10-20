#!/usr/bin/env python3
__author__ = 'tuhung-te'

from datetime import datetime
import time
import sys
import json
import re

import tweepy
import pycouchdb

import DBManager as db
import Settings as globalSettings
import Log as LogFucntions


class Streaming(object):
    def __init__(self,ckey,csec,atoken,asec,db_uri,logFileName):
        self.ckey = ckey;
        self.csec = csec;
        self.atoken = atoken;
        self.asec = asec;
        auth = tweepy.OAuthHandler(self.ckey,self.csec);
        auth.set_access_token(self.atoken,self.asec);
        self.auth = auth;
        self.server = pycouchdb.Server(db_uri);
        self.api = tweepy.API(self.auth)
        self.logFunctions = LogFucntions.Log(logFileName)

    def store_data(self,row,dbmanager):
            #test =dbmanager.isNotExisted(globalSettings.db_name,row["id_str"])
            self.logFunctions.logger.info("get recent ID: %s",row["id_str"])
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


class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status)

    def on_error(self, status_code):
        #print >> sys.stderr, 'Error:', status_code
        streamingAPI.logFunctions.logger.info("{} Error: {}".format(sys.stderr,status_code))
        #print("{} Error: {}".format(sys.stderr,status_code))
        return True

    def on_timeout(self):
        streamingAPI.logFunctions.logger.info("Timeout...Retry again")
        return True

    def on_data(self, raw_data):
         rows = json.loads(raw_data)
         streamingAPI.store_data(rows,dbmanager);
         streamingAPI.logFunctions.isTimeToChangeFileName()
         #if re.search(r'\bReal Estate\b | \bHOUSE AUCTIO(N|NS)\b | \bPROPERTY SALES\b',rows['text'],re.IGNORECASE):
         #   print(rows['text'])


streamingAPI = Streaming(globalSettings.auth_keys['jacky2'].ckey,globalSettings.auth_keys['jacky2'].csec,globalSettings.auth_keys['jacky2'].atoken,globalSettings.auth_keys['jacky2'].asec,globalSettings.db_uri,"Streaming",)
dbmanager = db.DBManager();

if __name__ == '__main__':
    tweets_amount = 100
    dbmanager.DBalive();
    while True:
        try:
            streamingAPI.logFunctions.logger.info("getting into streaming process")
            data = tweepy.Stream(streamingAPI.auth,CustomStreamListener())
            data.filter(locations=globalSettings.Mel_bounding_BOX)
            #data.filter(track=search_words,async=True)
        except tweepy.TweepError as e:
            print(e.reason)
        break






