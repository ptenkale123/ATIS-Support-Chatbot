from .api_wrappers.bing_search import get_first_result

def ground_transportation(locName):
    url, snippet = get_first_result("ground transportation for "+locName)
    print("I think this link might help you with that:")
    print(url)
    print("Quick description of the link:")
    print(snippet)


if __name__ == "__main__":
    ground_transportation("sfo")