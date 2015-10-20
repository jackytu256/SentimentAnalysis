#!/usr/bin/env python3
__author__ = 'tuhung-te'

import re

class settings:
    """
        Attributes for accessing twitter to get data
        1. CONSUMER_KEY
        2. CONSUMER_SEC
        3. ACCESS_TOKEN
        4. ACCESS_SEC
    """
    def __init__(self, ckey, csec, atoken, asec):
            self.ckey = ckey
            self.csec = csec
            self.atoken = atoken
            self.asec = asec




db_name = 'twitter_melbourne'
db_original_Name = 'twitter_org'
db_uri = 'http://115.146.94.232:5984'
db_follow_name = 'twitter_follow'
db_original_follow_Name ='twitter_follow_org'
geoRange_Area = '-37.8131869,144.9629796,30mi'
db_list=['twitter_melbourne','twitter_org','twitter_follow','twitter_follow_org','elasticsearch_auction',
         'analysis_result','analysis_result_angecies','houseingindex_bubble','house_price_income_ratio',
         'housepricewithrenterpayment','mortgagewithgdp']
#geoRange_Area = '144.9629796,--37.8131869,30mi'
search_users = [{'Name':'Jellis Craig','User_ID':85537208,'max_id':0,'count':0,'nodata':0},
                {'Name':'Andrew Wilson','User_ID':494552308,'max_id':0,'count':0,'nodata':0},
                {'Name':'spi_online','User_ID':114308197,'max_id':0,'count':0,'nodata':0}]

# Correct format is: SouthWest Corner(Long, Lat), NorthEast Corner(Long, Lat)
Mel_bounding_BOX =[144.394492,-38.260720,145.764740,-37.459846]


ElasticSearch_Config = {"server_ip":"130.56.248.244","port":80,"db_name":"elasticsearch_auction"}

stop_words_FileName = "stop_words.txt"


auth_keys ={
    'jacky':settings(
        "88s6B1UublCOVwRAxbAnKCI4Z",
        "xUjuYUA7immzqGpGCmR9YH4XTNLBRXVYVJVCVWYkhERZwwgTFP",
        "3180754530-RHk7GnQsNvUbDBEX6kvATVEFWEGbsnnWiAV6ODX",
        "2e43UNUqa6oCZfwFMym5rftu0LpBF5ML5ceGZ9tSw5mVs"
    ),

    'xin': settings(
        '04ERby2gwInEOTodxbLyGNbrZ',
        'poVkXJvOhnuwlc1AkaQuDWpO4N6YNZEmlB0YgS4rCRM1GHhOMQ',
        '2803020907-1d9ShXZ2tRzO1EzrP1QDyk42TpiOdubDnp7ekfa',
        'py2YB88r2YsP45gC7Fs3TbfVfxnG4Ef3gIn48gF5bepB0'
    ),

    'xin2': settings(
        'pwsPSOEtWTt2m1OO5wQAby3iW',
        'xIB4aM18OklGrtNqQjqFrugJUHUBTT274hn02TjUxAAAsI2Fa1',
        '2803020907-m2W3Q7WeDSSMcnh2rFgChLXuTxg0oYZQdRnUFnc',
        '7srtksL6zIIUVc29SzYYRuZIwFbU35mx0ExRSChOMvp0k'
    ),

    'nikvi': settings(
        'Gkov4WGDeIViDSct84klCJCoO',
        'xhdByIyeTSwU8byraNJg6b1RalyodjbILbhEsvSI0RRqMRUyh4',
        '47649768-W9aZXo9oQcQ8WYbYNn1YcEOaUrajxJrlAVne18VB2',
        'YorFM0a2VfgE6t7VffMpBfzPBbRul01a5tafJubi382h3'
    ),

    'zoey': settings(
        "JuDAs23ssLkzgGv7HAzA08Rfd",
        "R4xrvBWIzU1Mqd7BU13hX4AiHmzRqNQIJUhXNXZZYH661TIX6h",
        "808402454-1JJqi9TDziPasFusqXRoiFcYnvBOAyzcuCZMkZHT",
        "lbZjgJI7S44A1HZdYE2p13PoAdHyqDAkCFbZfG0EBsTNH"
    ),
     'jacky2': settings(
        "W3ENZkLF4Ek2e3t6VnVXBwBRE",
        "3ZClxvjieKH2txEb44SNJ11NBWahkEM5kZlCupGk99SKFvZs00",
        "3180754530-CEQ4tlx0iuD3tx7MfWEDx8H3ApxV1luVmzh8DkL",
        "sJaqzG7d2KT4qd8ORRBqJfDUD84YGvBe5OARMs1KWFvBn"
    )
}

search_Locations = [
    [-37.8131869,144.9629796],
    ["-37.8167","144.9879"],
    ["-37.8101","144.95"],
    ["-37.814","144.9633"],
    ["-37.8228","144.9643"]
]





DBMapping ={
    "analysis_Result_DB": lambda : "analysis_result",
    "all": lambda : {"view_Name":"sentiment_analysis/All","DB_Name":"analysis_result"},
    "allagencies": lambda : {"view_Name":"sentiment_analysis/All","DB_Name":"analysis_result_angecies"},
    "neg": lambda : {"view_Name":"sentiment_analysis/Neg","DB_Name":"analysis_result"},
    "neu": lambda : {"view_Name":"sentiment_analysis/Neu","DB_Name":"analysis_result"},
    "pos": lambda : {"view_Name":"sentiment_analysis/Pos","DB_Name":"analysis_result"},
    "negagencies": lambda : {"view_Name":"sentiment_analysis/Neg","DB_Name":"analysis_result_angecies"},
    "neuagencies": lambda : {"view_Name":"sentiment_analysis/Neu","DB_Name":"analysis_result_angecies"},
    "posagencies": lambda : {"view_Name":"sentiment_analysis/Pos","DB_Name":"analysis_result_angecies"},
    "negandpos": lambda : {"view_Name":"sentiment_analysis/NegAndPos","DB_Name":"analysis_result"},
    "allresult": lambda : {"view_Name":"sentiment_analysis/AllResults","DB_Name":"analysis_result"},
    "allagenciesresult": lambda : {"view_Name":"sentiment_analysis/AllResults","DB_Name":"analysis_result_angecies"},
    "percentage": lambda : {"view_Name":"sentiment_analysis/Percentage","DB_Name":"analysis_result"},
    "houseingindex": lambda : {"view_Name":"bubble/AllResult","DB_Name":"houseingindex_bubble"},
    "housepriceincome": lambda : {"view_Name":"bubble/AllResult","DB_Name":"house_price_income_ratio"},
    "housepricewithrenterpayment": lambda : {"view_Name":"bubble/AllResult","DB_Name":"housepricewithrenterpayment"},
    "mortgagewithgdp": lambda : {"view_Name":"bubble/AllResult","DB_Name":"mortgagewithgdp"}
}

Sentiment_Analysis_data = [
                           {"db":"twitter_follow","dataFrom": "sentiment_Analysis/Analysis","dataTo":"analysis_result_angecies"},
                           {"db":"twitter_melbourne","dataFrom": "sentiment_analysis/Perception_Property","dataTo":"analysis_result"},
                           {"db":"elasticsearch_auction","dataFrom": "elasticsearch/sentiment_Analysis","dataTo":"analysis_result"}]

excluded_Words =["market","property","housing","house","sydney"]