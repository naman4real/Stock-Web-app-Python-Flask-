from flask import Flask, request, jsonify
import requests
import datetime
from dateutil.relativedelta import relativedelta
import calendar
import os
headers = {
    'Content-Type': 'application/json'
}

application=Flask(__name__)

flag=0

@application.route("/")
def htmlFile():
    return application.send_static_file("index.html")


@application.route("/companyOutlook", methods=['GET'])
def companyOutlookTab():
    ticker=request.args.get('ticker')
    response = requests.get("https://api.tiingo.com/tiingo/daily/"+ticker+"?token=0331e1bdc9fb8f79fad5f2ccb5ee1c33bbda3205", headers=headers)   
    info=response.json()
    if not info:
        flag=1
        return "null"
    return info 

@application.route("/stockSummary", methods=['GET'])
def stockSummaryTab():   
    ticker=request.args.get('ticker')
    stockSummaryInfo={}   
    response = requests.get("https://api.tiingo.com/iex/"+ticker+"?token=0331e1bdc9fb8f79fad5f2ccb5ee1c33bbda3205", headers=headers)
    info=response.json()
    print(response.json())

    if not info:
        return "null"
    d=response.json()[0]  #length is 1
    stockSummaryInfo['Stock Ticker Symbol']=d['ticker']
    stockSummaryInfo['Trading Day']=d['timestamp']
    stockSummaryInfo['Previous Closing Price']=d['prevClose']
    stockSummaryInfo['Opening Price']=d['open']
    stockSummaryInfo['High Price']=d['high']
    stockSummaryInfo['Low Price']=d['low']
    stockSummaryInfo['Change']=float(d['last'])-float(d['open'])
    stockSummaryInfo['Change Percent']=(float(d['last'])-float(d['open']))/float(d['open'])*100
    stockSummaryInfo['Number of Shares Traded']=d['volume']
    return info[0]

@application.route("/chart")
def price_volume_Tab():  
    NOW = datetime.date.today()   
    ticker=request.args.get('ticker') 
    priorDate=str(NOW+relativedelta(months=-6))[:10]
    response = requests.get("https://api.tiingo.com/iex/"+ticker+"/prices?startDate="+priorDate+"&resampleFreq=12hour&columns=open,high,low,close,volume&token=0331e1bdc9fb8f79fad5f2ccb5ee1c33bbda3205", headers=headers)
    info=response.json()
    if info:
        return jsonify(info)
    return "null"

@application.route("/news")
def newsTab():
    ticker=request.args.get('ticker')
    response=requests.get("https://newsapi.org/v2/everything?apiKey=14fb46cfe59b415eba40be2047dadbad&q="+ticker,headers=headers)
    info=response.json()
    if not flag:
        return info
    return "null"

    
    
    
if __name__ == "__main__":
    application.run(debug=True)