# webapi_validchecker.py

# Ana Gao
# gaomy@uci.edu
# 26384258

from WebAPI import WebAPI
from LastFM import  LastFM
from OpenWeather import OpenWeather


def test_api(message:str, apikey:str, webapi:WebAPI):
    webapi.set_apikey(apikey)
    webapi.load_data()
    result = webapi.transclude(message)
    print(result)


open_weather = OpenWeather() #notice there are no params here...HINT: be sure to use parameter defaults!!!
lastfm = LastFM()

test_api("Testing the weather: @weather", '071481e600ad1194c116a0b9e95d56a8', open_weather)
# expected output should include the original message transcluded with the default weather value for the @weather keyword.

test_api("Testing lastFM: @lastfm", 'e05db7fa6efe7323ede21ee2e48c88f5', lastfm)
# expected output include the original message transcluded with the default music data assigned to the @lastfm keyword
