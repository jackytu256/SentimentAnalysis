#!/usr/bin/env python3
from flask import Flask,jsonify,render_template,request
from collections import Counter
import json
import time
import datetime
from operator import itemgetter
app = Flask(__name__)
from Tweet_Harvest.DBManager import DBManager as dbmanager
from Tweet_Harvest.Settings import DBMapping,excluded_Words

db = dbmanager()

def convertTime(time):
     convertime = datetime.datetime.strptime(time,'%a %b %d %H:%M:%S +0000 %Y')
     return "{}-{}".format(convertime.year,"0"+str(convertime.month) if convertime.month<10 else convertime.month)

def convertTimeToDate(time):
    convertime = datetime.datetime.strptime(time,'%a %b %d %H:%M:%S +0000 %Y')
    # for Google table chart time spec , every month will be added one automatically so that we need to minus 1.
    return 'Date({},{},{})'.format(convertime.year,convertime.month-1,convertime.day)

def converTimeISO8601(time):
    convertime = datetime.datetime.strptime(time,'%Y-%m-%d %H:%M:%S')
    return '{}-{}'.format(convertime.year,convertime.month-1)


# a web service provides three typs of results of sentiment analysis (neg,pos and neu)
@app.route('/analysis/ScatterData/<type>')
def getScatterData(type):
    db.dbName = DBMapping.get(str(type).lower(),lambda: "nothing")()["DB_Name"]
    db_view = DBMapping.get(str(type).lower(),lambda: "nothing")()["view_Name"]
    counter = Counter()
    resultsCount = Counter()
    data = None
    # "Percentage" needs to query by group
    if str(type).lower() =="percentage":
      data =list(db.getAllViewData(db_view,True))
    else:
      data = list(db.getAllViewData(str(db_view)))

    test = 0
    for rows in data:
        if rows.value:
                counter[rows.value] += 1
                #print(rows.value)
                test+=1


    data = {
        'cols': list(map(lambda x: {'id': x[0], 'label': x[0], 'type': x[1]}, [('Score', 'number'), ('Count', 'number')])),
        'rows': [{'c': [{'v': key}, {'v': val}]} for (key, val) in counter.items()]
    }
    return jsonify(data)

@app.route('/analysis/TrendData/<type>')
def getTrendData(type):
    db.dbName = DBMapping.get(str(type).lower(),lambda: "nothing")()["DB_Name"]
    db_view = DBMapping.get(str(type).lower(),lambda: "nothing")()["view_Name"]
    listdata =[]
    data = None
    test = 0
    # "Percentage" needs to query by group
    if str(type).lower() =="percentage":
      data =list(db.getAllViewData(db_view,True))
    else:
      data = list(db.getAllViewData(str(db_view)))

    for rows in data:
      if rows.value["sentiment"]["senti_Polarity"] >0:
         listdata.append([convertTime(rows.value["time"]),"pos"])
         test+=1
      elif rows.value["sentiment"]["senti_Polarity"] ==0:
         #listdata.append([convertTime(rows.value["time"]),"neu"])
         test+=1
      else:
         listdata.append([convertTime(rows.value["time"]),"neg"])
         test+=1
    # make list to be a three dimensional list ("2014-08-11",5,5 )
    templist = list(Counter([tuple(l) for l in listdata]).items())
    multituples = sorted(templist,key=lambda x:x[0][0])
    tempTime = ""
    tempPosCount = 0
    tempNegCount =0
    sentimentList = []
    for sentimentData in multituples:
        if tempTime == ""  or tempTime == sentimentData[0][0]:
             if sentimentData[0][1] == "pos":
                 tempPosCount = sentimentData[1]
             elif sentimentData[0][1] == "neg":
                 tempNegCount = sentimentData[1]

             tempTime = sentimentData[0][0]
        else:
            sentimentList.append({'c': [{'v': tempTime}, {'v': tempPosCount},{'v': tempNegCount}]})

            tempPosCount = 0
            tempNegCount = 0
            tempTime = sentimentData[0][0]
            if sentimentData[0][1] == "pos":
                 tempPosCount = sentimentData[1]
            elif sentimentData[0][1] == "neg":
                 tempNegCount = sentimentData[1]

    data = {
        'cols': list(map(lambda x: {'id': x[0], 'label': x[0], 'type': x[1]}, [('Year', 'string'), ('pos', 'number'),('neg', 'number')])),
        'rows': sentimentList
    }
    #print(sentimentList)
    return jsonify(data)


@app.route('/analysis/SentimentData/<type>')
def getIndividSentiemntResult(type):
    db.dbName = DBMapping.get(str(type).lower(),lambda: "nothing")()["DB_Name"]
    listdata =[]
    db_view = DBMapping.get(str(type).lower(),lambda: "nothing")()["view_Name"]
    data = list(db.getAllViewData(str(db_view)))
    #print(len(data))
    rows = [{'c': [{'v': convertTimeToDate(rows.value["time"])}, {'v': rows.value["text"]},{'v': rows.value["sentiment"]["perception"]}]} for rows in data]
    #rows = [[convertTimeToDate(rows.value["time"]),rows.value["text"],rows.value["sentiment"]["perception"]] for rows in data]
    data = {
        'cols': list(map(lambda x: {'id': x[0], 'label': x[0], 'type': x[1]}, [('Year', 'date'), ('text', 'string'),('sentiment', 'string')])),
        'rows': rows
    }
    #print(data)
    return jsonify(data)


# a web service provides a type (neg, neu and pos) dataset for getting most common words
@app.route('/analysis/result/most_comm/<type>')
def getMostComm(type):
    db.dbName =DBMapping.get(str(type).lower(),lambda: "nothing")()["DB_Name"]
    db_view = DBMapping.get(str(type).lower(),lambda: "nothing")()["view_Name"]
    word_list = []
    print(db_view)
    hasrows = True
    rowperpage = 300
    page = 0
    startid = " "
    most_comm = []
    returndata = []
    while hasrows:
        skip = 0 if page == 0 else 1
        page+=1
        data = db.query(db_view,rowperpage,skip,startid)

        if len(data)==0:
            break
        else:
            startid = data.rows[-1].value["id"]
        for words in data.rows:
            for singleword in words.value["correction"].split():
                if singleword not in excluded_Words:
                    most_comm.append((singleword))

    data ={
        'rows':[{'text': key, 'weight': val} for (key, val) in Counter(most_comm).most_common(20)]
    }
    #print(db_view)
    #print(data)
    ##### present the data based on the most_common
    return jsonify(data)



# provides detailed information of tweet based on the searchword
@app.route('/analysis/Sentiment/<type>')
def sMostCommonByKeyWord(type):
    db_view = DBMapping.get(str(type).lower(),lambda: "nothing")()
    searchword = request.args["searchword"] if "searchword" in request.args else "None"
    data = []
    hasrows = True
    rowperpage = 300
    page = 0
    startid = " "
    most_comm = []
    #print(db_view)
    while hasrows:
        skip = 0 if page == 0 else 1
        page+=1
        rows = [ x["value"] for x in db.query(db_view,rowperpage,skip,startid).rows if str(x["value"]["text"]).find(searchword)!= -1]
        if len(rows)==0:
            break
        else:
            startid =rows[-1]["id"]
            data.append(rows)


    return jsonify({"data":data})

@app.route('/analysis/Bubble/<type>')
def getBubbleHousingIndex(type):
    db.dbName = DBMapping.get(str(type).lower(),lambda: "nothing")()["DB_Name"]
    db_view = DBMapping.get(str(type).lower(),lambda: "nothing")()["view_Name"]
    data = list(db.getAllViewData(db_view))
    rows = [{'c': [{'v': converTimeISO8601(rows.value["date"])}, {'v': rows.value["index"]}]} for rows in data]
    data = {
        'cols': list(map(lambda x: {'id': x[0], 'label': x[0], 'type': x[1]}, [('Year', 'string'), ('index', 'number'),])),
        'rows': rows
    }
    #print(data)
    return jsonify(data)

@app.route('/analysis/HousePriceIncomeRatio/<type>')
def getHousePriceIncomeRatio(type):
    db.dbName = DBMapping.get(str(type).lower(),lambda: "nothing")()["DB_Name"]
    db_view = DBMapping.get(str(type).lower(),lambda: "nothing")()["view_Name"]
    data = list(db.getAllViewData(db_view))
    rows = [{'c': [{'v': converTimeISO8601(rows.value["date"])}, {'v': rows.value["ratio"]},{'v': rows.value["attribute"]['Annual_income']},{'v': rows.value["attribute"]['houseprice']}]} for rows in data]
    data = {
        'cols': list(map(lambda x: {'id': x[0], 'label': x[0], 'type': x[1]}, [('Year', 'string'),('House-price-income-ratio', 'number'), ('Annual Income', 'number'), ('House price', 'number')])),
        'rows': rows
    }
   # print(data)
    return jsonify(data)

@app.route('/analysis/HousePricewithRenterPayment/<type>')
def getHousePricewithRenterPayment(type):
    db.dbName = DBMapping.get(str(type).lower(),lambda: "nothing")()["DB_Name"]
    db_view = DBMapping.get(str(type).lower(),lambda: "nothing")()["view_Name"]
    data = list(db.getAllViewData(db_view))
    rows = [{'c': [{'v': rows.value["date"]}, {'v': rows.value["ratio"]},{'v': rows.value["attribute"]['renter_payment']},{'v': rows.value["attribute"]['houseprice']}]} for rows in data]
    data = {
        'cols': list(map(lambda x: {'id': x[0], 'label': x[0], 'type': x[1]}, [('Year', 'string'),('House Price Rent Ratio', 'number'), ('Annual renter payment', 'number'), ('House price', 'number')])),
        'rows': rows
    }
    #print(data)
    return jsonify(data)

####  render template below ##########
@app.route('/')
def base():
    return  render_template("Base.html")

@app.route('/Agencies_Sentiment')
def Agencies_Sentiment():
    return  render_template("Agencies_Sentiment.html")

@app.route('/Individuals_Sentiment')
def Individuals_Sentiment():
    return  render_template("Individuals_Sentiment.html")

@app.route('/Comparison')
def Comparison():
    return  render_template("Comparison.html")

@app.route('/House_Price_Index')
def House_Price_Index():
    return  render_template("House_Price_Index.html")

@app.route('/Agency_Comparison')
def Agency_Comparison():
    return  render_template("Agency_Comparison.html")

@app.route('/test')
def test():
    return  render_template("test.html")

@app.route('/House_Price_Income_Ratio')
def House_Price_Income_Ratio():
    return  render_template("House_Price_Income_Ratio.html")

@app.route('/House_Price_With_Renter_Payment')
def House_Price_With_Renter_Payment():
    return  render_template("House_Price_With_Renter_Payment.html")

@app.route('/MortgageGDP')
def MortgageGDP():
    return  render_template("MortgageGDP.html")

@app.route('/System_Architecture')
def System_Architecture():
    return  render_template("System_Architecture.html")


if __name__ == '__main__':
    app.debug = True
    app.run()

