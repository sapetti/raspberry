#!/usr/bin/env python
# -*- coding: utf-8 -*-
from facepy import GraphAPI#, GraphAPIError
import requests

ACCESS_TOKEN = '[[ACCESS_TOKEN]]'
graph = GraphAPI(ACCESS_TOKEN)

# Post a photo of a parrot
graph.post(
    path = '645856582167140/photos',
    source = open('CF008593.jpg')
)

