import requests

BING_SEARCH_API_URL = 'https://api.bing.microsoft.com/v7.0/search'

BING_API_KEY = '9d6c5d50278b4ecba10c7d191b8c87b1'

def get_first_result(queryStr):
    searchRes = requests.get(BING_SEARCH_API_URL, headers={'Ocp-Apim-Subscription-Key': BING_API_KEY}, params={'q':queryStr}).json()
    return searchRes['webPages']['value'][0]['url'], searchRes['webPages']['value'][0]['snippet']
