import requests
import csv
import json
import pymongo
import pandas as pd
from datetime import datetime
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# authenticate API
client_auth = requests.auth.HTTPBasicAuth('QcKi1s7adyI-MTGN2Bw5QQ', 'wNOxSS0oybPjisjOuxvwc6vXXFMxJQ')
data = {
    'grant_type': 'password',
    'username': 'One_Young_7786',
    'password': 'Harsha6597'
}
headers = {'User-Agent': 'myproj/0.0.1'}

# send authentication request for OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=client_auth, data=data, headers=headers)
# extract token from response and format correctly
TOKEN = f"bearer {res.json()['access_token']}"
# update API headers with authorization (bearer token)
headers = {**headers, **{'Authorization': TOKEN}}

# we use this function to convert responses to dataframes
def df_from_response(res):
    # initialize temp dataframe for batch of data in response
    df = pd.DataFrame()

    # loop through each post pulled from res and append to df
    for post in res.json()['data']['children']:
        df = df.append({
            'subreddit': post['data']['subreddit'],
            'title': post['data']['title'],
            'selftext': post['data']['selftext'],
            'ups': post['data']['ups'],
            'downs': post['data']['downs'],
            'score': post['data']['score'],
            'created_utc': datetime.fromtimestamp(post['data']['created_utc']).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'id': post['data']['id'],
            'kind': post['kind']
        }, ignore_index=True)

    return df



# initialize dataframe and parameters for pulling data in loop
data = pd.DataFrame()
params = {'limit': 100}

#r = ['Coronavirus','COVID19positive','COVID19_support','China_Flu','COVID19','CovidVaccinated']
r = pd.read_csv("subred.csv")
# loop through 10 times (returning 1K posts)
for redd in r['title']:
    # make request
    print(redd)
    for i in range(5):
        url = "https://oauth.reddit.com/r/%s/new" % redd
        res = requests.get(url,
                       headers=headers,
                       params=params)
        print(url)
        #print(res.json())
        new_df = df_from_response(res)
    # append new_df to data
        data = data.append(new_df, ignore_index=True)
    # get dataframe from response
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = client["nawab_db"]
        mycol = mydb["Reddit"]  
        #x = mycol.insert_many(res.json()['data']['children'])
        new_df.reset_index(inplace=True)
        new_df_dict = new_df.to_dict("records")
        mycol.insert_many(new_df_dict)
    
    # take the final row (oldest entry)
        row = data.iloc[len(data)-1]
        #print(len(data))
    # create fullname
        if(i!=4):
            fullname = row['kind'] + '_' + row['id']
    # add/update fullname in params
            params['after'] = fullname
        else:
            fullname=0
            params['after'] = fullname
print(data)

