#!/usr/bin/env python3
__author__ = 'tuhung-te'
import couchdb
from Tweet_Harvest.Settings  import db_uri,db_name,auth_keys,search_Locations,db_original_Name,db_follow_name,db_original_follow_Name,db_list
import functools

class DBManager(object):

    def __init__(self):
     self.db_uri = db_uri
     self.server = couchdb.Server(db_uri)
     self.dbName = db_name
     self.dbOrg_data = db_original_Name
     self.auth_keys = auth_keys
     self.search_locations = search_Locations
     self.db_follow_name = db_follow_name
     self.db_original_follow_Name =db_original_follow_Name
     self.db = None


    def DBalive(self):
        isAlive = False
        try:
            for dbnames in db_list:
                if dbnames not in list(self.server):
                    self.server.create(dbnames)

        except couchdb.PreconditionFailed:
            print(couchdb.PreconditionFailed.with_traceback())

    def transaction(self,data,storeIn):
        self.db =self.server[storeIn]
        return self.db.save(data)



    def isNotExisted(self,db_name,id):
        return self.server[db_name].get(id) is None

    def getViewData(self,view_name,group=False):
        db = self.server[self.dbName]
        return db.view(view_name,group=group)

    def query(self,query,limited,skip,startdoc):
        db = self.server[self.dbName]
        return db.view(query,limit=limited,skip=skip,startkey=startdoc,startkey_docid=startdoc)

    def getAllViewData(self,view_name,group=False):
        data = []
        hasrow = True
        rowperpage = 300
        page = 0
        startid = ""
        startkey =""
        db = self.server[self.dbName]
        while hasrow:
            skip = 0 if page == 0 else 1
            rows = db.view(view_name,limit=rowperpage,skip=skip,startkey=startid,startkey_docid=startid)
            page+=1
            for row in rows:
              startid = row.id
              data.append(row)

            if len(rows._rows) ==0:
                hasrow = False

        return data

