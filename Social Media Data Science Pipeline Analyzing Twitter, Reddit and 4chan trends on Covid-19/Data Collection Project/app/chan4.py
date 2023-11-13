import requests
from datetime import datetime
import pandas
import json
import csv
from time import gmtime, strftime
import time
import pymongo
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

timestamp=time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime())

r = requests.get('https://a.4cdn.org/sp/catalog.json', headers={"If-Modified-Since": 'timestamp' })
print(r.status_code)
if(r.status_code != 200):
    print("HTTP response 429 returned")
    exit()
        
r = r.json()

csvFile = open("chan.csv", "a", newline="", encoding='utf-8')
csvWriter = csv.writer(csvFile)
csvWriter.writerow(['text','resto','time','fname','url','sendata'])
csvFile.close()

client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = client["nawab_db"]
mycol = mydb["chan"]


def gen_chan():
    for idx, page in enumerate(r):
        for thread in r[idx]['threads']:
            yield thread


def append_to_csv(res, fileName):
    #Open OR create the target CSV file
    csvFile = open(fileName, "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)
        
    # Append the result to the CSV file
    csvWriter.writerow(res)
    csvFile.close()

def get_threads(key: str, default='NaN'):
    return threads.get(key, default)


for threads in gen_chan():
    if 'last_replies' in threads:
        for comment in threads['last_replies']:
            text = comment.get('com', 'NaN')
            resto = comment.get('resto', 'NaN')
            now = comment.get('now', 'NaN')
            time = comment.get('time', 'NaN')
            fname = comment.get('filename')
            url = comment.get('com')
            sentdata = comment.get('com')
            #df = pandas.DataFrame(now_com,resto_com)
            result = [text,now,fname]
            res = {"text":text,"now":now,"fname":fname}
            #print(res)
            df = pandas.DataFrame(result)
            data = pandas.DataFrame()
            data = data.append(df)
            append_to_csv(result,"chan.csv")
            #load_to_db(data)
            #records = json.loads(new_df.T.to_json()).values()
            #data.reset_index(inplace=True)
            #new_df_dict = data.to_dict("records")
            mycol.insert_one(res)
            



    
