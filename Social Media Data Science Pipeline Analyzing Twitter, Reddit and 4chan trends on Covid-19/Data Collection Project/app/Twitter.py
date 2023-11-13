import requests
import os
import csv
from pandas import DataFrame
import json
import pymongo


# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = "AAAAAAAAAAAAAAAAAAAAALoWiQEAAAAAGn%2FYZZedXhYn%2B3nBkV7gtZTJt0w%3D3MeY1ZHlMUVtcj9F5iAoiCLo0pDlpj6UBX8HTvSqgL8RoOafGO"

def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    #print(json.dumps(response.json()))
    return response.json()

def append_to_csv(json_response, fileName):
    #A counter variable
    counter = 0

    #Open OR create the target CSV file
    csvFile = open(fileName, "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)

    t_id = json_response['data']['id']

    text = json_response['data']['text']
        
    res = [t_id, text]
        
        # Append the result to the CSV file
    csvWriter.writerow(res)
     # counter += 1
    csvFile.close()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post("https://api.twitter.com/2/tweets/search/stream/rules",auth=bearer_oauth,json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    #print(json.dumps(response.json()))


def set_rules(delete):
    # You can adjust the rules if needed
    sample_rules = [
        {"value": "covid","lan":"eng"},
        {"value": "coronavirus", "lan":"eng"},
        {"value": "COVID-19", "lan":"eng"},
        {"value": "pandemic", "lan":"eng"},
        {"value": "VACCINES", "lan":"eng"},
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    #print(json.dumps(response.json()))


def get_stream(set):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", auth=bearer_oauth, stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    count = 0
    data = DataFrame()
    for response_line in response.iter_lines():
        count = count+1
        if response_line:
            json_response = json.loads(response_line)
            #print(json.dumps(json_response, indent=4, sort_keys=True)
            
            s = json_response['data']['text']
            if(s.startswith("RT @")):
                count = count-1
                continue
            else:
                append_to_csv(json_response,"data.csv")
                df = DataFrame(json_response['data'])
                data = data.append(df)
                client = pymongo.MongoClient("mongodb://localhost:27017/")
                mydb = client["nawab_db"]
                mycol = mydb["twitter"]  
                #mycol.insert_one(data)


                x = mycol.insert_one(json_response)
                print(x)
            #print("coun=",count)
        if(count >= 100000):
           break;
        print(data)


def main():
    rules = get_rules()
    delete = delete_all_rules(rules)
    set = set_rules(delete)
    get_stream(set)


if __name__ == "__main__":
    csvFile = open("data.csv", "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(['Id','tweet'])
    csvFile.close()
    main()