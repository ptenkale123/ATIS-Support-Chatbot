from .api_wrappers.get_abbreviation import get_abbreviation

def abbreviation(abbr, entityName):
    entityType = ""
    if entityName == "airport_code":
        entityType = "airports"
    elif entityName == "airline_code":
        entityType = "airlines"
    elif entityName == "aircraft_code":
        entityType = "aircrafts"

    meaning = get_abbreviation(abbr, entityType)
    if entityType == "":
        print("Ehh can't help you get the meaning of that abbreviation... Sorry :/")
    else:
        meaning = get_abbreviation(abbr, entityType)
        meaningLen = len(meaning)
        if (meaningLen == 0):
            print("I wasn't able to find the meaning of "+abbr+" in my "+entityType+" database.")
            print("I think you should try using Google. Sorry :/")
        elif (meaningLen == 1):
            print("I believe "+abbr+" stands for "+meaning[0])
        elif (meaningLen == 2):
            print("Meaning of "+abbr+":")
            print(meaning[0]+", "+meaning[1])


if __name__ == "__main__":
    abbreviation("sfo", "airport_code")
    print('')
    abbreviation("ua", "airline_code")
    print('')
    abbreviation("dc10", "aircraft_code")
    print('')
    abbreviation("dc10", "airport_code")
