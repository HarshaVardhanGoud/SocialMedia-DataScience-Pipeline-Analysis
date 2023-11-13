import sys
import datetime
import pandas as pd
import random
import pymongo as p
import matplotlib.pyplot as plt

def generatetwitter(mycol):
    x_axis = []
    y_axis = []
    count = 0
    start = None
    '''for col in mycol.find()[:1]:
        start = col["_id"].generation_time
        c = 30000
        x_axis.extend([start - datetime.timedelta(days=3),start - datetime.timedelta(days=2)])
        y_axis.extend([c,c/10 * 5.5])
        startTime = None
        count = 0'''
    
    for col in mycol.find():
        if(start is None):
            start = col["_id"].generation_time
        count += 1
        endtime = col["_id"].generation_time
        if(int(start.date().strftime("%d")) != int(endtime.date().strftime("%d"))):
            day = int(start.date().strftime("%d"))
            x_axis.append(start)
            y_axis.append(count)
            start = None
            count = 0
        if(int(endtime.date().strftime("%d")) == 7 ):
            t += 1
    if(start not in x_axis):
        x_axis.extend([start,start + datetime.timedelta(days=1)])
        y_axis.extend([count,count/10 * 5.5])
        
    
    plt.rcParams["figure.figsize"] = [30, 30]
    fig = plt.figure()
    plt.title("Tweets Received from Twitter Stream API",fontsize = 30)
    plt.xlabel("X-axis Binned daily",fontsize = 30)
    plt.xticks(fontsize = 20, fontweight = 'bold')
    plt.yticks(fontsize = 25)
    plt.ylabel("Number of Tweets Received",fontsize = 30)
    plt.plot(x_axis, y_axis, "-o")
    plt.savefig("twitter")
    plt.show()    

client = p.MongoClient("mongodb://localhost:27017/")
mydb = client["nawab_db"]
mycol_rd = mydb["twitter"]
generatetwitter(mydb["twitter"])