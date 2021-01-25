from .api_wrappers.google_maps import get_coordinates, get_physical_distance, get_route_distance

# try google distance matrix. If that doesn't work then do physical distance

def distance_two_locations(location1Str, location2Str):
    print("Want to know the distance from "+location1Str+" to "+location2Str+"? Not a problem! Give me a second.")
    location1Coor = get_coordinates(location1Str)
    location2Coor = get_coordinates(location2Str)
    routeDist = get_route_distance(location1Coor, location2Coor)
    if routeDist != {}:
        print("The driving distance for that route is "+str(routeDist))
    else:
        physicalDist = get_physical_distance(location1Coor, location2Coor)
        print("The geographical distance between the two locations is appr "+str(round(physicalDist, 1))+" km")
        print("To be honest, I'm not sure how much time it would take to fly between those two locations, but I think this website might help:")
        print("https://flighttime-calculator.com")

def distance_one_location(locationStr):
    location2Str = locationStr+" airport"
    distance_two_locations(locationStr, location2Str)


if __name__ == "__main__":
    distance_two_locations("San Francisco", "San Mateo")
    print('')
    distance_two_locations("San Francisco", "Mumbai")
    print('')
    distance_one_location("Los Angeles")