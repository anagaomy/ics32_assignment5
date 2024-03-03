# openweather.py

# Ana Gao
# gaomy@uci.edu
# 26384258


import urllib
import json
import urllib.request
import urllib.error
import requests.exceptions
import datetime


class OpenWeather:

    def __init__(self, zipcode, ccode):
        self.zipcode = zipcode
        self.ccode = ccode

    def set_apikey(self, apikey:str) -> None:
        self.apikey = apikey

    def load_data(self) -> None:
        response = None
        r_obj = None
        request_url = f"http://api.openweathermap.org/data/2.5/weather?zip={zip},{self.ccode}&appid={self.apikey}"

        try:
            response = urllib.request.urlopen(request_url)
            json_results = response.read()
            r_obj = json.loads(json_results)

            self.temperature = r_obj["main"]["temp"]
            self.high_temperature = r_obj["main"]["temp_max"]
            self.low_temperature = r_obj["main"]["temp_min"]
            self.longitude = r_obj["coord"]["lon"]
            self.latitude = r_obj["coord"]["lat"]
            self.description = r_obj["weather"]["description"]
            self.humidity = r_obj["main"]["humidity"]
            self.city = r_obj["name"]
            self.sunset = datetime.datetime.fromtimestamp(r_obj["sys"]["sunset"]).strftime('%H:%M')   

        except requests.exceptions.ConnectionError:
            raise Exception("Please check your internet connection")

        except urllib.error.HTTPError as e:
            status_code = e.code

            if status_code == 404:
                raise Exception("The specified URL is not valid. Please check your zipcode and country code.")
            elif status_code == 503:
                raise Exception("The remote API is unavailable. Please try again later.")
            else:
                raise Exception("An unknown error has occurred. Please try again later.")

        except urllib.error.URLError:
            raise Exception("Cannot connect to the internet. Please check your connection and try again.")

        except json.decoder.JSONDecodeError:
            raise Exception("Invalid data from remote API.")
        
        finally:
            if response != None:
                response.close()

        return r_obj


# def main() -> None:
    # zip = "92697"
    # ccode = "US"
    # apikey = "071481e600ad1194c116a0b9e95d56a8"
    # url = f"http://api.openweathermap.org/data/2.5/weather?zip={zip},{ccode}&appid={apikey}"

    # try:
        # weather_obj = OpenWeather(zip, ccode)
        # if weather_obj is not None:
            # print(weather_obj['weather'][0]['description'])
            # print(weather_obj)

    # except Exception as e:
        # print("Error:", e)


# if __name__ == '__main__':
    # main()
