import datetime
import math
import json
import csv
from textblob import TextBlob
import pymongo as pm
import time
from bson.objectid import ObjectId
import warnings
from flask import Flask,render_template,request

app = Flask(__name__)

@app.route("/")
def hello():
  return render_template("home.html")

@app.route("/Subi")
def sentiment_plot():
    twit, red, cha = 0,0,0
    client = pm.MongoClient("mongodb://localhost:27017/")
    mydb = client["nawab_db"]
    chan = mydb["chan"]
    reddit = mydb["Reddit"]
    twitter = mydb["twitter"]
    args = request.args
    
    for val in twitter.find({"_id": {"$gte": objectIdWithTimestamp(mydb,args["sd"],datetime.timedelta(days = 0)),"$lte":objectIdWithTimestamp(mydb,args["ed"],datetime.timedelta(days = 2))}}).limit(200):
        twit += TextBlob(val["data"]["text"]).subjectivity
    for val in reddit.find({"_id": {"$gte": objectIdWithTimestamp(mydb,args["sd"],datetime.timedelta(days = 0)),"$lte":objectIdWithTimestamp(mydb,args["ed"],datetime.timedelta(days = 2))}}).limit(200):
        red += TextBlob(val["title"]).subjectivity
    for val in chan.find({"_id": {"$gte": objectIdWithTimestamp(mydb,args["sd"],datetime.timedelta(days = 0)),"$lte":objectIdWithTimestamp(mydb,args["ed"],datetime.timedelta(days = 2))}}).limit(200):
        cha += TextBlob(val["text"]).subjectivity
    polarities = [twit/200,red/200,cha/200]
    return render_template("temp.html", pol= polarities)

def objectIdWithTimestamp(db, timestamp, delta):
    # /* Convert string date to Date object (otherwise assume timestamp is a date) */
    timestamp = ( datetime.datetime.strptime( timestamp,"%m/%d/%Y" )) + delta
    constructedObjectId = ObjectId.from_datetime(timestamp)
    return constructedObjectId

@app.route("/dcp")
def up_plot():
    args = request.args
    client = pm.MongoClient("mongodb://localhost:27017/")
    mydb = client["nawab_db"]
    mycol = mydb["Reddit"]
    count = 0
    x_axis = []
    y_axis = []
    startTime = None
    
    for item in mycol.find({"_id": {"$gte": objectIdWithTimestamp(mydb,args["sd"],datetime.timedelta(days = 0)),"$lte":objectIdWithTimestamp(mydb,args["ed"],datetime.timedelta(days = 2))}}):
        endTime = item["_id"].generation_time
        if(startTime is None):
            startTime = endTime   
        count += int(item["ups"]) 
        if(endTime.strftime("%d/") != startTime.strftime("%d/")):
            x_axis.append(startTime.strftime("%m/%d/%Y"))
            y_axis.append(count)
            startTime = None
            count = 0    
            
    return render_template("up_plot.html", x=x_axis,y=y_axis)                 



if __name__ == "__main__":
    app.run(port=5000, debug=True, host="0.0.0.0")
