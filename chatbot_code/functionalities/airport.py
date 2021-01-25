from .api_wrappers.bing_search import get_first_result

def specific_airport(airportName):
    print("Looking for information on "+airportName+"? Not a problem! Give me a second.")
    url, snippet = get_first_result(airportName+" official website")
    print("I think this link might help you with that:")
    print(url)


def list_airports(cityName):
    print("Looking for airports in "+cityName+"? Not a problem! Give me a second.")
    url, snippet = get_first_result("list of airports in "+cityName)
    print("I think this link might help you with that:")
    print(url)


if __name__ == "__main__":
    specific_airport("sfo")
    list_airports("San Francisco")
