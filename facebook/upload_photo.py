
import re

#from django.conf import settings
#import facepy
from facepy import GraphAPI

#graph = get_application_graph_api()
# Initialize the Graph API for a user:
#graph = GraphAPI(oauth_token)

# Initialize the Graph API for an application:
graph = GraphAPI(
    client_id = '[[APP_ID]]',
    client_secret = '[[APP_SECRET]]'
)

# Post a photo of a parrot
graph.post(
    path = '[[ALBUM_PATH]]',
    source = open('PHOTO.jpg')
)
