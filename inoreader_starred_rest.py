#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import re
import flask
import os

Email = os.environ.get("INOREADER_EMAIL")
Passwd = os.environ.get("INOREADER_PASSWORD")
AppId = os.environ.get("INOREADER_APP_ID")
AppKey = os.environ.get("INOREADER_APP_KEY")

Output = 'json'

TokenURL = f'https://www.inoreader.com/accounts/ClientLogin?Email={Email}&Passwd={Passwd}'
TokenRegex = r'Auth=(.*)'

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():

    TokenResponse = requests.post(TokenURL)

    Token = re.compile(TokenRegex, re.MULTILINE).search(
        TokenResponse.text).group(1)

    JSONRequestHeader = {'Authorization': f'GoogleLogin auth={Token}'}

    continuation = ''
    InfoItems = []

    while True:

        JSONURL = f'https://www.inoreader.com/reader/api/0/stream/contentsuser/-/state/com.google/starred?n=100&output={Output}&AppId={AppId}&AppKey={AppKey}&c={continuation}'

        JSONResponse = requests.get(JSONURL, headers=JSONRequestHeader)
        CurrentInfoDict: dict = json.loads(JSONResponse.text)
        CurrentItems: list = CurrentInfoDict.get('items')

        if len(InfoItems) != 0 and InfoItems[0].get('id') == CurrentItems[0].get('id'):
            break

        InfoItems.extend(CurrentItems)
        continuation = CurrentInfoDict.get("continuation")

    return {'items': InfoItems}


app.run()
