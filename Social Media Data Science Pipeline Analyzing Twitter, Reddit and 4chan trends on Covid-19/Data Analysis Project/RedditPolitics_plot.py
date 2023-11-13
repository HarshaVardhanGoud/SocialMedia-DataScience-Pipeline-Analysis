import sys
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import random
import pymongo as p


def generatePolitics(mycol):
    x_axis = []
    y_axis = []
    start = None
    count = 0
    
    for col in mycol.find():
        if(start is None):
            start = col["_id"].generation_time
        count += 1
        endtime = col["_id"].generation_time 
        if((endtime - start).total_seconds() / 60 > 60):
            x_axis.append(start)
            y_axis.append(count)
            start = None
            count = 0
        if(int(endtime.date().strftime("%d")) >= 14 ):
            break
    
    plt.rcParams["figure.figsize"] = [20, 20]
    fig = plt.figure()
    plt.title("Number of Posts Received from Subreddit Politics",fontsize = 30)
    plt.xlabel("Dates binned every Hour",fontsize = 30)
    plt.xticks(fontsize = 20, fontweight = 'bold')
    plt.yticks(fontsize = 25)
    plt.ylabel("Number of Posts Received",fontsize = 30)
    plt.plot(x_axis, y_axis, "-o")
    plt.savefig("Politics")
    plt.show()    

client = p.MongoClient("mongodb://localhost:27017/")
mydb = client["nawab_db"]
generatePolitics(mydb["Rd"])