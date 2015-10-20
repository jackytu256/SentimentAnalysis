__author__ = 'tuhung-te'
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from elasticsearch_dsl.connections import connections
from Settings import  ElasticSearch_Config
import DBManager as db
from datetime import datetime
import time
import json
connections.create_connection(hosts=['130.56.248.244'],port=80)

class eSearch(object):

    # querystructure is not extensible ( need a flexible string as a input parameter)
    # the way I can fix it is that I can embed string
    def __init__(self,pagesize,index,doc_type,querystring,From=None):
        self.dbmanager = db.DBManager()
        self.index = index
        self.doc_type =doc_type
        self.pagesize = pagesize if pagesize else 100
        self.From = 0 if From is None else From
        self.querystring = querystring
        self.queryStructure ={
                    "query":querystring,
                    "from": self.From,
                    "size": self.pagesize
                }
    # should not fix the query structure cuz the users may need to query data by several key words.
    # this method will return totalcount and data
    def search(self):
        es = Elasticsearch([{'host': ElasticSearch_Config['server_ip'],'port':ElasticSearch_Config['port']}])
        query = self.queryStructure
        data = es.search(index=self.index,doc_type=self.doc_type,body=query)
        # for row in data["hits"]["hits"]:
        #    #print(json.dumps(row))
        #    print(self.From)
        return data["hits"]["total"],data["hits"]["hits"]

    def count(self):
        es = Elasticsearch([{'host': ElasticSearch_Config['server_ip'],'port':ElasticSearch_Config['port']}])
        query = self.queryStructure
        data = es.search(index=self.index,doc_type=self.doc_type,body=query,search_type="count")

    def storeData(self,data,storein):
         for row in data:
              if self.dbmanager.isNotExisted(storein,row["_source"]["doc"]["id_str"]):
                  self.dbmanager.transaction(row["_source"]["doc"],storein)

    def updateQueryStructure(self):
        self.From+= self.pagesize
        self.queryStructure = {
                    "query": self.querystring,
                    "from": self.From,
                    "size": self.pagesize
                }


    def searchbyfield(self):
          es = Elasticsearch([{'host': ElasticSearch_Config['server_ip'],'port':ElasticSearch_Config['port']}])
          query ={"query":{"filtered": {
                            "query": {
                                "bool": {
                                    "must": [
                                        {
                                            "query_string": {
                                                "fields" : ["doc.entities.hashtags.text"],
                                                "query": "negative gearing"
                                            }
                                        },
                                    ]
                                }
                            },
                            "filter": {
                                "bool": {
                                    "must": [
                                        {
                                            "match_all": {}
                                        }
                                    ]
                                }
                            }
                        }
                    },"from": self.From,
                     "size": self.pagesize
          }
          data = es.search(index=self.index,doc_type=self.doc_type,body=query)
          print(data["hits"]["total"])
          return data["hits"]["total"],data["hits"]["hits"]


    def DSL(self):
        s = Search(index=self.index,doc_type=self.doc_type).query("term",_source="auctions")
        data = s.execute()
        return data

if __name__ == '__main__':

     totalcount = 0
     currentcount = 0
     querystring ={"filtered": {
                            "query": {
                                "bool": {
                                    "should": [
                                        {
                                            "query_string": {
                                                "query": "negative gearing"
                                            }
                                        }
                                    ]
                                }
                            },
                            "filter": {
                                "bool": {
                                    "must": [
                                        {
                                            "match_all": {}
                                        }
                                    ]
                                }
                            }
                        }
                    }
     elasticSearch = eSearch(300,"es","melbourne",querystring)
     elasticSearch.dbmanager.DBalive()
     #elasticSearch.searchbyfield()
     #elasticSearch.DSL();
     while True:
         try:

             totalcount,data = elasticSearch.search();
             elasticSearch.storeData(data,ElasticSearch_Config['db_name'])
             if currentcount>=totalcount:
                 elasticSearch.From = 0
                 currentcount = 0
             else :
                 currentcount += elasticSearch.pagesize
                 elasticSearch.updateQueryStructure()

             print(str.format("total:{} ----- current:{}",totalcount,currentcount))

         except RuntimeError as e:
             e.with_traceback()



