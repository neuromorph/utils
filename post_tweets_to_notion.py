#!/usr/bin/python3 -u
"""
Script to send liked/bookmarked tweets of a user to Notion database. 
First export liked tweets to a json file using get_tweets.py
Create a database in Notion (if not exists) with Properties as available in the json file. 
Same properties should be populated in code below. Default values here are:
    Username, URL, Tweet Id, Tweet Text, Created At, Referenced Tweets(Contains tweet Ids of quoted, retweeted or replied to tweets)
You need to get your Notion secret token and the Notion database Id.
"""

import requests
import json
from tqdm import tqdm
import sys

NOTION_TOKEN = "<NOTION_TOKEN>"
NOTION_DB_ID_LIKES = "<NOTION_DB_ID_LIKES>"
NOTION_DB_ID_BOOKMARKS = "<NOTION_DB_ID_BOOKMARKS>"


def main():

    if sys.argv[1] == 'likes':
        jfile = 'likes.json'
        NOTION_DB_ID = NOTION_DB_ID_LIKES
        print("Exporting Liked tweets to Notion")
    else:
        jfile = 'bookmarks.json'
        NOTION_DB_ID = NOTION_DB_ID_BOOKMARKS
        print("Exporting Bookmarked tweets to Notion") 


    url = f'https://api.notion.com/v1/pages'

    payload = {
        "parent": {
        "type": "database_id",
        "database_id": NOTION_DB_ID
        },
        "properties": {
        'User Name':{},
        'URL':{},
        'Full Text':{},
        'Quoted Full Text':{},
        'Created At':{},
        'Id':{}
        }
    }


    with open(jfile, 'r') as jsonfile:
        jtweets = json.load(jsonfile)

    # count = 0
    for tweet in tqdm(jtweets['tweets']):
        payload['properties']['User Name']['type'] = 'title'
        payload['properties']['User Name']['title'] = [{ "type": "text", "text": { "content": tweet["username"] } }]
        payload['properties']['URL']['type'] = "url"
        payload['properties']['URL']['url'] = tweet["URL"]
        payload['properties']['Full Text']['type'] = "rich_text"
        payload['properties']['Full Text']['rich_text'] = [{ "type": "text", "text": { "content": tweet["text"]} }]
        payload['properties']['Quoted Full Text']['type'] =  "rich_text"
        payload['properties']['Quoted Full Text']['rich_text'] = [{ "type": "text", "text": { "content": str(tweet["referenced_tweets"])} }]
        payload['properties']['Created At']['type'] = "rich_text"
        payload['properties']['Created At']['rich_text'] =  [{ "type": "text", "text": { "content":tweet["created_at"]} }]
        payload['properties']['Id']['type'] = "rich_text"
        payload['properties']['Id']['rich_text'] =  [{ "type": "text", "text": { "content":tweet["id"]} }]

        r = requests.post(url, headers={
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }, data=json.dumps(payload))

        # print(r.json())
        # count += 1
        # if count >1:
        #     break
    print(f"Successfully exported {len(jtweets['tweets'])} tweet-{sys.argv[1]} to Notion")

 
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Argument missing. Please specify what you want to export: likes or bookmarks \n e.g. python3 post_tweets_to_notion.py likes')
        sys.exit(1)

    if not (sys.argv[1] == 'likes' or sys.argv[1] == 'bookmarks'):
        print('Incorrect argument. Please specify what you want to export: likes or bookmarks \n e.g. python3 post_tweets_to_notion.py likes')
        sys.exit(1)
    
    main()
