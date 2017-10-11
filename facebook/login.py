import re

from django.conf import settings
import facepy

def get_application_graph_api():
    kwargs = {
        'client_id': '[[APP_ID]]',
        'client_secret': '[[APP_SECRET]]',
        'grant_type': 'client_credentials',
    }
    access_token_string = facepy.GraphAPI().get('oauth/access_token', **kwargs)
    print access_token_string
    match = re.match(r"^access_token=(?P<access_token>.*)$", access_token_string)
    if match:
        return facepy.GraphAPI(match.groups()[0])
    raise facepy.FacepyError('no access_token in response')


get_application_graph_api()
