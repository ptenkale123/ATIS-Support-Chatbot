from datetime import datetime

FLIGHT_NO_BASE_URL = 'https://www.kayak.com/tracker/'

def specific_flight(airlineCode, flightNum):
    airlineCode = airlineCode.upper()
    flightNum = str(flightNum)
    print("I think the link below might help you find information for flight "+airlineCode+" "+flightNum)
    todayStr = datetime.today().strftime('%Y-%m-%d')
    print(FLIGHT_NO_BASE_URL+airlineCode+"-"+flightNum+"/"+todayStr)

def flight_routes():
    print("So you're looking to book a flight? Yeah, I'm not smart enough to help you with that. I think you should go to kayak.com. Sorry.. :/")


if __name__ == "__main__":
    specific_flight("ua", 2344)