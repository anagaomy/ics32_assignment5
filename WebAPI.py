# webapi.py

# Ana Gao
# gaomy@uci.edu
# 26384258


import urllib
import json
import urllib.request
import urllib.error
import requests.exceptions
from abc import ABC, abstractmethod


class WebAPI(ABC):

    def __init__():
        pass

    def _download_url(self, url: str) -> dict:
        response = None
        r_obj = None

        try:
            response = urllib.request.urlopen(url)
            json_results = response.read()
            json_results = json_results.decode(encoding='utf-8')
            r_obj = json.loads(json_results)

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
        
        except Exception as e:
            print('Error:', e)
        
        finally:
            if not response is None:
                response.close()

        return r_obj

    def set_apikey(self, apikey:str) -> None:
        self.apikey = apikey

    @abstractmethod
    def load_data(self):
      pass

    @abstractmethod
    def transclude(self, message:str) -> str:
        pass
