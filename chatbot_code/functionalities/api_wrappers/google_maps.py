import requests
import math
from .api_keys import GOOGLE_API_KEY

PLACE_API_URL = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
DIST_MATRIX_API_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json'

def get_coordinates(placeStr):
    placeRes = requests.get(PLACE_API_URL, params={'key':GOOGLE_API_KEY, 'query':placeStr}).json()
    # print(placeRes)
    if (placeRes['status'] != 'OK'):
        return {}
    location = placeRes['results'][0]['geometry']['location']
    return (location['lat'], location['lng'])

R = 6371000 # metres

def get_physical_distance(location1, location2):
    if (len(location1) < 2 or len(location2) < 2):
        return {}
    lat1 = location1[0]
    lat2 = location2[0]
    lon1 = location1[1]
    lon2 = location2[1]
    phi1 = lat1 * math.pi/180 # phi in radians
    phi2 = lat2 * math.pi/180
    deltaPhi = (lat2-lat1) * math.pi/180
    deltaLambda = (lon2-lon1) * math.pi/180

    a = math.sin(deltaPhi/2) * math.sin(deltaPhi/2) + \
            math.cos(phi1) * math.cos(phi2) * \
            math.sin(deltaLambda/2) * math.sin(deltaLambda/2)
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    d = R * c # in metres

    return (d / 1000) # return km version of it

def get_route_distance(location1, location2):
    if (len(location1) < 2 or len(location2) < 2):
        return {}
    location1Str = str(location1[0]) + ', ' + str(location1[1])
    location2Str = str(location2[0]) + ', ' + str(location2[1])
    distMatrixRes = requests.get(DIST_MATRIX_API_URL, params={'key':GOOGLE_API_KEY, 'origins':location1Str, 'destinations': location2Str}).json()
    if (distMatrixRes['rows'][0]['elements'][0]['status'] == 'OK'):
        return distMatrixRes['rows'][0]['elements'][0]['distance']['text']
    else:
        return {}


if __name__ == "__main__":
    print(get_physical_distance((37.6213129, -122.36840685), (37.5629917,  -122.3255254)))
    print(get_route_distance(get_coordinates('SFO'), get_coordinates('San Mateo')))
