import requests
# Zenpy accepts an API token
creds = {
    'email' : 'sreerajpaalat@gmail.com',
    'token' : 'sn4QGuY81QyHAQctLXY3jRILhKrJQWEGRsJb4oRC',
    'subdomain': 'sreerajpalat'
}



# Or a password
creds = {
    'email' : 'sreerajpaalat@gmail.com',
    'password' : 'Palat@1570',
    'subdomain': 'sreerajpalat'
}

# Import the Zenpy Class
from zenpy import Zenpy

# Default
zenpy_client = Zenpy(**creds)

# Alternatively you can provide your own requests.Session object
zenpy_client = Zenpy(**creds, session=requests.Session())

# If you are providing your own HTTPAdapter object, Zenpy provides defaults via the
# Zenpy.http_adapter_kwargs() method. You can choose to use these defaults like so:
# session = requests.Session()
# session.mount('https://', MyAdapter(**Zenpy.http_adapter_kwargs()))
# zenpy_client = Zenpy(**creds, session=some_session)