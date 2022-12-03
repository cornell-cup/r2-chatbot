'''
This file calls a restaurant API and a geocoding API (getting latitude and
longitude coordinates)
'''

import requests
import geocoder

KEY = ""
UNITS = "units="

GEONAMES_USERNAME = ""

def lookup_restaurant(lat, lng):
    '''
    Looks up the nearby restaurants for a certain coordinate
    location

    @param lat: a string for the latitude
    @param lng: a string for the longitude

    @return: the full json data from the API call
    '''
    url = "https://developers.zomato.com/api/v2.1/geocode?"+"&lat="+lat+"&lon="+lng
    header= {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": KEY}
    response= requests.get(url,headers=header)


    return response.json()

def lookup_restaurant_city(city):
    '''
    Convenience function that converts city name into lat, lng.
    Calls lookup_restaurant() and returns output

    @param city: city name. Should include more specific info as needed (country, state, etc.)
    If empty string, returns empty string

    @return: if city is specified, the full json data from the API call. Otherwise empty string
    '''
    if city == "":
        return ""
    
    lat, lng = city_to_coord(city)
    return lookup_restaurant(lat, lng)

def import_keys():
    '''
    Imports all of the necessary API keys
    '''

    global KEY, GEONAMES_USERNAME

    #geonames APIs
    #with open("/home/systemslab/Desktop/chatbot/r2-chatbot/r2_chatterbot/api_keys/geonames_username.txt") as f:
    with open("api_keys/geonames_username.txt") as f:
        GEONAMES_USERNAME = f.read().strip()

    #open restaurant API
    #with open("/home/systemslab/Desktop/chatbot/r2-chatbot/r2_chatterbot/api_keys/restaurant_api.txt") as f:
    with open("api_keys/restaurant_api.txt") as f:
        KEY = f.read().strip()

def city_to_coord(city_string):
    '''
    Geocodes a city name into latitude, longitude coordinates

    @param city_string: the name of the city

    @return: A tuple with (latitude, longitude)
    '''
    print("restaurant coord\n\n")
    g = geocoder.geonames(city_string, key=GEONAMES_USERNAME)
    return (g.lat, g.lng)

import_keys()

if __name__ == "__main__":
    coords = city_to_coord("ithaca new york")
    nearby_restaurants = lookup_restaurant(coords[0], coords[1])
    print(nearby_restaurants)
