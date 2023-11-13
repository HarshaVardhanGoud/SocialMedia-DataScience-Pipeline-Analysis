Before you start working on README:
* If your project have `README.md` file (in the format described below.), you earn 10 extra-points for project1 implementation section.
* This is just a sample `README` and you must change(and allowed to change) everything according to your project.
* Please do not ask any questions, what should and should not be included in `README.md`. Think about if you hand-over project to someone, what needs to be told to run and use your project! 🙂

## Project Abstract

  The main objective of this project is to collect the data from three sources which are Twitter, Reddit, 4chan using there API's. The three different crawler codes is built to extract the data from the three data sources. In twitter we are collecting ID's and text. Reddit we will collect posts from a specific number of subreddits.
  In 4chan we will collect th posts, comments and threads from specific boards. All these data which is collected will be stored in Mongodb database.



## Tech-stack

* `python` - The project is developed and tested using python v3.8. [Python Website](https://www.python.org/)
* `request` - Request is a popular HTTP networking module(aka library) for python programming language. [Request Website](https://docs.python-requests.org/en/latest/#)
* `MondoDB`- This project uses Mongodb database for saving collected data. 
* [Python-pymongo](https://pymongo.readthedocs.io/en/stable/)
*  `warnings` - to remove warnings from console while the code is running.
* `pandas` & `matplotlib` - Pandas, Matplotlib is not being used in actual crawler. It is being used just for collected data analysis.
* `csv` - CSV is used to covert the collected data to .csv format for analysis in future.
* `json` - we need to import as the data requested from API will be in json format.

**NOTE: You must include all 3rd-party tools used in the project(Every single of it.) e.g., Numpy, pandas, etc.**

## Three data-source documentation

This section must include two things for each source: (1) A specific end-point URL(aka API) or Website link if you are crawling web-pages (2) Documentation of the API

* `Twitter`
  * [Volume Stream API](https://api.twitter.com/2/tweets/search/stream/rules) - < A regular 1% volume stream API from Twitter.>
  * (https://developer.twitter.com/en/docs/twitter-api/tweets/volume-streams/introduction) Documentation of the API

* `Reddit` - We are ucollecting data from theses specific reddits like
  * Documentation of the API - (https://www.reddit.com/dev/api/)
  * [r/covid](https://reddit.com/r/covid) - <collect new posts from this specific reddit>
  * [API-1](https://oauth.reddit.com/r/%s/new) - <Here %s will be replaced by subreddit name>

* `4chan` - <Small description goes here. Yada, yada, yada...>
  * [API-Link](https://a.4cdn.org/sp/catalog.json) - <we are using catalog api to extract posts from 4chan>
  * [Website-link](https://www.4chan.org/) - <Read the Documentation for 4chan API>

## System Architecture

![System Architecture](https://docs.google.com/document/d/1iR6zB8JUehkeR28wJyDEEYLMZQNiIO_fSBDPMfjMTA0/edit?usp=sharin)


**NOTE: You can create something like this with [Lucid-charts](https://www.lucidchart.com/pages/) but you can use whatever is easy for you. Do not copy this architecture which is created by professor.**

## How to run the project?

Install `Python` and `MongoDB`

```bash
pip install pandas, numpy,
pip install csv,
pip install time,
pip install warnings,
pip install json,
pip install pymongo,
cd home/hmarago1/
python3 Reddit.py
```
Note:For reddit it takes subreddit names from 'subred.csv' file and generate data from those specific reddits. Please include this file while running reddit data collection program.

**NOTE: You must mention all required details to run your project. We will not fix any `compilation` or `runtime` error by ourself. If something needs to be installed, mention it!**

## Database schema - SQL (Remove this section if you are using NoSQL database)

**Reference for Twitter from docs:  https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Filtered-Stream/filtered_stream.py

table1_name: twitter_volume_stream

| Edit History id (pk) | id | text | 
| ------ | ------ | ------ | ------ 
| integer | integer | text| 

table2_name: reddit_comments

|  Subreddit | title | selftext | ups | downs | score | created_utc | id  | kind |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ----- | ----- |
| text | text | text | integer | integer | integer | timestamp | integer | varchar(25) |

table3_name: 4chan_posts

| Post | Timestamp | Filename |
| ------ | ------ | ------ | 
| text | timestamp | varchar(25) |

**NOTE: You can have as many tables you want with whatever schema, we don't care. You need to mention the data-schema you created, that's it!**

## Database schema - NoSQL (Remove this section if you are using SQL database)

```bash

collection_1: twitter_volume
{
  "EDit History id": ...,
  "id": ...,
  "Tweet": ...
}

collection_2: reddit_comments
{
  "Subreddit": ...,
  "title": ...,
  "selftext": ...
  "ups": ...,
  "downs": ...,
  "score": ...,
  "created_utc": ...,
  "id": ...,
  "kind": ...,
}

collection_3: 4chan_posts
{
  "Post/comment": ...,
  "timestamp": ...,
  "Filename": ...
}
```

**NOTE: You can have as many collections you want with whatever fields in document, we don't care. NoSQL is schemaless, but still add fields you are collecting, that's it!**

## Special instructions for us???

If no notes, Congratulations, that's your first data-collection system running at scale! 😎

