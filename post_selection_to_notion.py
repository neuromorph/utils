#!/usr/bin/python3 -u
"""
Script to send any selected text on your desktop to Notion database with keyboard shortcut.
You can add this command to a custom keyboard shortcut:
    sh -c "/usr/bin/python3 <path to this python file>"
Select some text and press the keyboard shortcut. A pop up appears where you can optionally add comma seperated tags.

Required properties should be populated in code below. Default values here are: Selected text, tags

You need to get your Notion secret token and the Notion database Id and update below.
"""

import requests
import json
import subprocess

NOTION_TOKEN = "<NOTION_TOKEN>"
NOTION_DB_ID_HIGHLIGHTS = "<NOTION_DB_ID_HIGHLIGHTS>"


def main():

    url = f'https://api.notion.com/v1/pages'

    payload = {
        "parent": {
        "type": "database_id",
        "database_id": NOTION_DB_ID_HIGHLIGHTS
        },
        "properties": {
        'Note Text':{},
        'Source':{},
        'Tags':{}
        }
    }

    note_text = subprocess.check_output([
        "/usr/bin/bash", 
        "-c",
        "xsel -o"]).decode("utf-8")

    # print(note_text)
    
    try:
        note_tags = subprocess.check_output([
            "/usr/bin/bash", 
            "-c",
            "zenity --entry --title='Notion Notes' --text='Tags'"]).decode("utf-8").split(",")
        # print("res",note_tags)
        if note_tags == ['\n']:
            note_tags = [{"name":"Untagged"}]
        else:
            note_tags = [{"name": x.strip()} for x in note_tags]
    except:
        note_tags = [{"name":"Untagged"}]
    
    # print(note_tags)

    payload['properties']['Note Text']['type'] = 'title'
    payload['properties']['Note Text']['title'] = [{ "type": "text", "text": { "content": note_text } }]

    payload['properties']['Source']['type'] = "rich_text"
    payload['properties']['Source']['rich_text'] = [{ "type": "text", "text": { "content": ""} }] # Source is not yet implemented

    payload['properties']['Tags']['type'] = "multi_select"
    payload['properties']['Tags']['multi_select'] = note_tags       

    r = requests.post(url, headers={
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }, data=json.dumps(payload))

    # print(r.json())

# def get_page_property():
#     pageid = "2660fbc901044386b273f6d0c60de4f2"
#     property_id = "PgTm"
#     url = f'https://api.notion.com/v1/pages/{pageid}/properties/{property_id}'
#     r = requests.get(url, headers={
#         "Authorization": f"Bearer {NOTION_TOKEN}",
#         "Notion-Version": "2022-06-28",
#         "Content-Type": "application/json"
#     })

#     print(r.json())
 
if __name__ == '__main__':   
    main()