from collections import defaultdict
from functionalities.ground_transportation import *
from functionalities.flight import *
from functionalities.distance import *
from functionalities.airport import *
from functionalities.abbreviation import *
import requests

NLU_MODEL_URL = 'http://localhost:5005/model/parse'

def getNLURes(inputStr):
    inputData = '{"text":"'+inputStr+'"}'
    NLUres = requests.post(NLU_MODEL_URL, data=inputData)
    NLUres = NLUres.json()
    return (NLUres['intent'], NLUres['entities'])

def printIntent(intent):
    print("INTENT:", intent)

def printEntities(entities):
    print("ENTITIES:")
    print(entities)

# have some methods which check if it particular entities are present

# have method to extract city

# method to extract date

if __name__ == "__main__":
    print("Hello! I am the ATIS Support Chatbot! How can I help you today?")
    print('')

    while (True):
        userInput = input("")

        if userInput == "exit()":
            break

        print('')

        intent, entitiesList = getNLURes(userInput)
        intent = intent['name']

        # for entities: make a dictionary with { entity -> { value -> freq } }

        entities = {}

        for entityObj in entitiesList:
            value = entityObj['value']
            entity = entityObj['entity']
            periodIdx = entity.find('.')
            if (periodIdx >= 0):
                superEntity = entity[:periodIdx]
                rawEntity = entity[(periodIdx+1):]
                if superEntity not in entities:
                    entities[superEntity]= {}
        
                if rawEntity not in entities[superEntity]:
                    entities[superEntity][rawEntity] = {}

                if value not in entities[superEntity][rawEntity]:
                    entities[superEntity][rawEntity][value] = 0
                
                entities[superEntity][rawEntity][value] += 1
                
            else:
                if entity not in entities:
                    entities[entity] = {}

                if value not in entities[entity]:
                    entities[entity][value] = 0
                
                entities[entity][value] += 1
        
        # for debugging:
        printIntent(intent)
        printEntities(entities)
        print('')

        if intent == "flight":
            # get information about flights from one location to another
            flight_routes()
        elif intent == "airfare":
            if "airline_code" in entities and "flight_number" in entities:
                # get information about a specific flight
                specific_flight(list(entities["airline_code"].keys())[0], list(entities["flight_number"].keys())[0])
            else:
                # get information from one flight to another 
                flight_routes()

        elif intent == "ground_service":
            # get information about ground transportation for specific city or airport name
            entityName = ""
            if "city_name" in entities:
                entityName = "city_name"
            elif "airport_name" in entities:
                entityName = "airport_name"
            elif "airport_code" in entities:
                entityName = "airport_code"
            
            if entityName != "":
                ground_transportation(list(entities[entityName].keys())[0])
            else:
                print("Could you re-enter the query and specify exactly what city/airport you'd like ground transportation information?")

        elif intent == "airline":
            # Two possible intents:
            # - get airlines for flight from one location to another (same entities as flight)
            # - get airline with specific code (same as abbreviation)

            if "airline_code" in entities:
                # get meaning of abbreviation
                abbreviation(list(entities["airline_code"].keys())[0], "airline_code")
            else:
                # get information about flights from one location to another
                flight_routes()

        elif intent == "abbreviation":
            # 1 entity
            # Possible entities: airport_code, airline_code, fare_basis_code, restriction_code, meal_code
            # Response detailed in notes

            # get meaning of abbreviation

            entityName = ""
            if "airport_code" in entities:
                entityName = "airport_code"
            elif "airline_code" in entities:
                entityName = "airline_code"
            elif "fare_basis_code" in entities:
                entityName = "fare_basis_code"
            elif "restriction_code" in entities:
                entityName = "restriction_code"
            elif "meal_code" in entities:
                entityName = "meal_code"
            elif "aircraft_code" in entities:
                entityName = "aircraft_code"
            
            if entityName != "":
                abbreviation(list(entities[entityName].keys())[0], entityName)
            else:
                print("Could you re-enter the query and specify the abbreviation you'd like to find the information to?")

        elif intent == "aircraft":
            # Three Possible Intents: 
            # - aircraft of a specific flight (airline_name, flight_number)
            # - aircraft of a specific abbreviation (aircraft_code, similar to abbreviation) 
            # - aircraft of a flight (from one location to another, same entities as flight)

            if "airline_code" in entities and "flight_number" in entities:
                # get information about a specific flight
                specific_flight(list(entities["airline_code"].keys())[0], list(entities["flight_number"].keys())[0])
            elif "aircraft_code" in entities:
                # get meaning of abbreviation
                abbreviation(list(entities["aircraft_code"].keys())[0], "aircraft_code")
            else:
                # get information about flights from one location to another
                flight_routes()

        elif intent == "flight_time":
            # get information about flights from one location to another
            flight_routes()

        elif intent == "quantity":
            # generic 'IDK' response
            print("Can't help you with quantities buddy. Use Google")
        elif intent == "airport":
            # request will only have 1 entity: city_name, airport_name, or state_name
            # for city_name or state_name -> Google Search Engine API("list of airports in [INSERT city/state]")
            # for airport_name -> Google Search Engine API("[INSERT airport] official website")

            if "city_name" in entities or "state_name" in entities:
                if "city_name" in entities:
                    list_airports(list(entities["city_name"].keys())[0])
                else:
                    list_airports(list(entities["state_name"].keys())[0])
            elif "airport_name" in entities:
                specific_airport(list(entities["airport_name"].keys())[0])
            else:
                print("Could you re-enter the query and specify exactly what city/state/airport you'd like information for?")

        elif intent == "distance":
            # Figure out if it's distance of flight from one city to another OR distance from airport to city downtown
            # then use Places API (get coordinates of locations) + Google Distance Matrix API (distance between coordinates)

            # if there are 2 entities: just get coordinates of both and use google distance matrix api
            # if it's only 1 entity: there calculate airport of city to downtown of city (fromloc.city_name OR fromloc.airport_name)

            entityFound = True

            def get_location_string(locEntities):
                if "city_name" in locEntities:
                    return list(locEntities["city_name"].keys())[0]
                elif "airport_name" in locEntities:
                    return list(locEntities["airport_name"].keys())[0]
                elif "airport_code":
                    return list(locEntities["airport_code"].keys())[0]
                else:
                    return ""

            if "fromloc" in entities and "toloc" in entities:
                # get distance between two locations
                fromloc = get_location_string(entities["fromloc"])
                toloc = get_location_string(entities["toloc"])
                if fromloc == "" or toloc == "":
                    entityFound = False
                else:
                    distance_two_locations(fromloc, toloc)
            elif "fromloc" in entities:
                # get distance between airport and downtown of city
                if "city_name" in entities["fromloc"]:
                    distance_one_location(list(entities["fromloc"]["city_name"].keys())[0])
                else:
                    entityFound = False
            elif "city_name" in entities:
                # get distance between airport and downtown of city
                distance_one_location(list(entities["city_name"].keys())[0])
            else:
                entityFound = False

            if not entityFound:
                print("Could you re-enter the query and specify which two locations you'd like the distance for?")

        elif intent == "city":
            # generic 'IDK' response
            print("Can't help you with cities buddy. Use Google")
        elif intent == "ground_fare":
            # Pretty much the same as ground_service
            # get information about ground transportation for specific city or airport name
            entityName = ""
            if "city_name" in entities:
                entityName = "city_name"
            elif "airport_name" in entities:
                entityName = "airport_name"
            elif "airport_code" in entities:
                entityName = "airport_code"
            
            if entityName != "":
                ground_transportation(list(entities[entityName].keys())[0])
            else:
                print("Could you re-enter the query and specify exactly what city/airport you'd like ground transportation information?")

        elif intent == "capacity":
            # generic 'IDK' response
            print("Can’t help you for seating capacity buddy. Use Google")
        elif intent == "flight_no":
            # Same criteria as flight
            # get information about flights from one location to another
            flight_routes()
        elif intent == "restriction":
            # generic 'IDK' response
            print("I actually don’t know much about restriction codes, I think you should consult this site: http://www.scdmvonline.com/Driver-Services/Commercial-Licenses/CDL-Restriction-Codes. Or just google it.")
        elif intent == "meal":
            # generic 'IDK' response
            print("Can’t help you for specific meal information buddy. Use Google")
        else:
            print("I couldn't figure out what you're asking for. Could you repeat that?")

        print('')

