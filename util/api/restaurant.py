'''
This file calls a restaurant API and a geocoding API (getting latitude and
longitude coordinates)
'''

import requests
import geocoder


# r = requests.get(
#   "https://developers.zomato.com/api/v2.1/geocode?lat=41.10867962215988&lon=29.01834726333618", 
#   headers={"user_key": "MY_API_KEY_HERE", "Accept": "application/json"});

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

def import_keys():
    '''
    Imports all of the necessary API keys. Call this before using
    other functionality of this module
    '''
    
    global KEY, GEONAMES_USERNAME

    #geonames API
    with open("api_keys/geonames_username.txt") as f:
        GEONAMES_USERNAME = f.read().strip()
    
    #openweather API
    with open("api_keys/restaurantAPI.txt") as f:
        KEY = f.read().strip()

def city_to_coord(city_string):
    '''
    Geocodes a city name into latitude, longitude coordinates

    @param city_string: the name of the city

    @return: A tuple with (latitude, longitude)
    '''
    
    g = geocoder.geonames(city_string, key=GEONAMES_USERNAME)
    return (g.lat, g.lng)

if __name__ == "__main__":
    import_keys()

    coords = city_to_coord("ithaca new york")
    nearby_restaurants = lookup_restaurant(coords[0], coords[1])
    print(nearby_restaurants)

