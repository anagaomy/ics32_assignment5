# openweather.py

# Ana Gao
# gaomy@uci.edu
# 26384258


import urllib
import json
import urllib.request
import urllib.error
import requests.exceptions


def _download_url(url_to_download: str) -> dict:
    response = None
    r_obj = None

    try:
        response = urllib.request.urlopen(url_to_download)
        json_results = response.read()
        r_obj = json.loads(json_results)

    except urllib.error.HTTPError as e:
        print("Failed to download contents of URL")
        print("Status code: {}".format(e.code))

    finally:
        if response != None:
            response.close()
    
    return r_obj


class OpenWeather:

    def set_apikey(self, apikey:str) -> None:
        '''
        Sets the apikey required to make requests to a web API.
        :param apikey: The apikey supplied by the API service
            
        '''
        #TODO: assign apikey value to a class data attribute that can be accessed by class members
        pass


    def load_data(self) -> None:
        '''
        Calls the web api using the required values and stores the response in class data attributes.
            
        '''
        #TODO: use the apikey data attribute and the urllib module to request data from the web api. See sample code at the begining of Part 1 for a hint.
        #TODO: assign the necessary response data to the required class data attributes

        try: 
            pass

        except requests.exceptions.ConnectionError:
            raise Exception("Please check your internet connection")

        except urllib.error.HTTPError:
            raise Exception("City not found, please try again.")

        except urllib.error.URLError:
            raise Exception("Cannot connect to the internet. Please check your connection and try again.")

        except json.decoder.JSONDecodeError:
            raise Exception("Invalid data from remote API.")


def main() -> None:
    zip = "92697"
    ccode = "US"
    apikey = "071481e600ad1194c116a0b9e95d56a8"
    url = f"http://api.openweathermap.org/data/2.5/weather?zip={zip},{ccode}&appid={apikey}"

    try:
        weather_obj = _download_url(url)
        if weather_obj is not None:
            print(weather_obj['weather'][0]['description'])
            # print(weather_obj)

    except Exception as e:
        print("Error:", e)


if __name__ == '__main__':
    main()
