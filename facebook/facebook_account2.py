#!/usr/bin/env python
# -*- coding: utf-8 -*-
from facepy import GraphAPI#, GraphAPIError
import requests

FACEBOOK_APP_ID = '[[APP_ID]]'
FACEBOOK_APP_SECRET = '[[APP_SECRET]]'

r = requests.get('https://graph.facebook.com/oauth/access_token?grant_type=client_credentials&client_id='+FACEBOOK_APP_ID+ '&client_secret='+FACEBOOK_APP_SECRET)
ACCESS_TOKEN = r.text.split('=')[1]
print ACCESS_TOKEN
graph = GraphAPI(ACCESS_TOKEN)

# Post a photo of a parrot
graph.post(
    path = '[[ALBUM_PATH]]',
    source = open('PHOTO.jpg')
)

