import requests
from .api_keys import BING_API_KEY

BING_SEARCH_API_URL = 'https://api.bing.microsoft.com/v7.0/search'

def get_first_result(queryStr):
    searchRes = requests.get(BING_SEARCH_API_URL, headers={'Ocp-Apim-Subscription-Key': BING_API_KEY}, params={'q':queryStr}).json()
    return searchRes['webPages']['value'][0]['url'], searchRes['webPages']['value'][0]['snippet']
