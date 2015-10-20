__author__ = 'tuhung-te'
import Sentiment_Analysis.PreProcessing as preprocessing
import couchdb
import DBManager
from Settings import db_name,Sentiment_Analysis_data
import textblob
import json


class Analysis(object):

    def __init__(self):
        self.dbmanager = DBManager.DBManager()

    def savedata(self,data,id,storeIn):
         if self.dbmanager.isNotExisted(storeIn,id):
             self.dbmanager.transaction(data,storeIn)





if __name__ == '__main__':
 pprocessing =preprocessing.PreProcessing()
 analysis = Analysis()
 analysis.dbmanager.DBalive();
 #analysis.dbmanager.dbName = ElasticSearch_Config["db_name"]
 #analysis.dbmanager.dbName = db_name
 #data =dbmanager.getViewData("elasticsearch/sentiment_Analysis")
 hasrow = True
 rowperpage = 100
 page = 0
 startid = ""
 startkey =""
 for row in Sentiment_Analysis_data:
     dataFrom = row["dataFrom"]
     dataTo = row["dataTo"]
     analysis.dbmanager.dbName = row["db"]
     while hasrow:
         skip = 0 if page == 0 else 1
         #rows = analysis.dbmanager.query("elasticsearch/sentiment_Analysis",rowperpage,skip,startid)
         rows = analysis.dbmanager.query(dataFrom,rowperpage,skip,startid)
         page+=1
         for row in rows:
             startid = row.id
             perception = None
             print(startid)
             print(row.value[0]["text"])
             text = textblob.TextBlob(pprocessing.processing(row.value[0]["text"]))
             print(str.format("correction:{}",text))
             if text.sentiment.polarity >0:
                 perception = "pos"
             elif text.sentiment.polarity ==0:
                 perception = "neu"
             else:
                 perception = "neg"
             parsed_json =  dict(row.value[0])
             parsed_json["sentiment"] = {"senti_Polarity":text.sentiment.polarity,"sent_subjectivity":text.sentiment.subjectivity,"perception": perception}
             parsed_json["_id"] = row.id
             parsed_json["correction"] = text.string
             analysis.savedata(parsed_json,row.id,dataTo)
             print(text.sentiment)
             print(text.sentiment.polarity)

         if len(rows._rows) ==0:
            hasrow = False









