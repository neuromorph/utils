#!/usr/bin/python3 -u
"""
Script to export liked/bookmarked tweets of a user to a json file.
You need your Twitter Bearer Token and User Id for auth and getting tweets.
The tweet details to export are as per the 'data' parameter below. Default values here are:
Username, URL, Tweet Id, Tweet Text, Created At, Referenced Tweets(Contains tweet Ids of quoted, retweeted or replied to tweets)
Uses Twitter API V2 with Python requests module.
The Twitter response object contains a dictionary with 'data', 'includes' and 'meta'. 
data - List of tweets with associated details
includes - Contains 'users' as list of user ids and their names, and 'tweets' as list of referenced tweets
meta - Contains result count and 'next_token' which is to be passed as pagination_token for next page

"""

import requests
import json
from tqdm import tqdm
import sys
 
BEARER_TOKEN_LIKES = "<TWEETER_BEARER_TOKEN_LIKES>"
BEARER_TOKEN_BOOKMARKS = "<TWEETER_BEARER_TOKEN_BOOKMARKS>"
ID = "<TWEETER_USER_ID>"
USERNAME = "<TWEETER_USER_NAME>"


def main():

    if sys.argv[1] == 'likes':
        url = f"https://api.twitter.com/2/users/{ID}/liked_tweets"
        jfile = 'likes.json'
        BEARER_TOKEN = BEARER_TOKEN_LIKES
        print("Exporting Liked tweets")
    else:
        url = f"https://api.twitter.com/2/users/{ID}/bookmarks"
        jfile = 'bookmarks.json'
        BEARER_TOKEN = BEARER_TOKEN_BOOKMARKS
        print("Exporting Bookmarked tweets")  

    headers = { "Authorization" : F"Bearer {BEARER_TOKEN}", "Content-Type": "application/json; charset=utf-8" }

    data = {
        "tweet.fields": "created_at,id,text",
        "user.fields": "name,username", 
        "expansions": "author_id,referenced_tweets.id",
        "max_results": 100
        }  

    page_count = 0
    tweet_count = 0
    tweets_dict = {"tweets":[]}
    response = {'meta':{'next_token':''}}
    users = []

    while 'next_token' in response['meta']:

        if response['meta']['next_token'] != '':
            data['pagination_token'] = response['meta']['next_token']

        res = requests.get(url, headers=headers, params=data)
        response = res.json()
        # print(response)
        if 'data' not in response:
            break
        
        users += response['includes']['users']

        page_count += 1
        print(f"Page {page_count}:")

        for tweet in tqdm(response['data']):
            tweet['username'] = next((item['name'] for item in users if item['id'] == tweet['author_id']), tweet['author_id'])
            tweet['URL'] = f"https://twitter.com/{USERNAME}/status/{tweet['id']}"
            if 'referenced_tweets' not in tweet:
                tweet['referenced_tweets'] = ""   
            tweets_dict["tweets"].append(tweet)

        tweet_count += len(response['data'])

        for tweet in tqdm(response['includes']['tweets']):
            tweet['username'] = next((item['name'] for item in users if item['id'] == tweet['author_id']), tweet['author_id'])
            tweet['URL'] = f"https://twitter.com/{USERNAME}/status/{tweet['id']}"
            if 'referenced_tweets' not in tweet:
                tweet['referenced_tweets'] = "" 
            tweets_dict["tweets"].append(tweet)

        tweet_count += len(response['includes']['tweets'])
        
        # if page_count > 2:
        #     break

    jtweets = json.dumps(tweets_dict)

    with open(jfile, 'at', buffering=1) as jsonfile:
        jsonfile.write(jtweets)

    print(f"Successfully exported {tweet_count} tweet-{sys.argv[1]} to {jfile}")
    
    # with open('favs.json', 'r') as jfile:
    #     json.load(jfile)



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Argument missing. Please specify what you want to export: likes or bookmarks \n e.g. python3 get_tweets.py likes')
        sys.exit(1)

    if not (sys.argv[1] == 'likes' or sys.argv[1] == 'bookmarks'):
        print('Incorrect argument. Please specify what you want to export: likes or bookmarks \n e.g. python3 get_tweets.py likes')
        sys.exit(1)
    
    main()
    
    
