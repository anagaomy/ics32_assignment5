# lastfm.py

# Ana Gao
# gaomy@uci.edu
# 26384258

import urllib
import json
import urllib.request
import urllib.error
import requests.exceptions
from datetime import datetime


class LastFM:

    def __init__(self, user) -> None:
        self.user = user

    def set_apikey(self, apikey:str) -> None:
        self.apikey = str(apikey)

    def set_limit(self, limit=50) -> None:
        self.limit = str(limit)
    
    def set_page(self, page=1) -> None:
        self.page = str(page)

    def _download_url(self, url_to_download: str) -> dict:
        response = None
        parsed_response = None

        try:
            response = urllib.request.urlopen(url_to_download)
            response_body = response.read()
            response_body = response_body.decode(encoding='utf-8')
            parsed_response = json.loads(response_body)

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
            if not response is None:
                response.close()

        return parsed_response

    def load_data(self) -> None:
        request_url = str("http://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user=" +
                          self.user + "&api_key=" + self.apikey + "&limit=" +
                          self.limit + "&page=" + self.page + "&format=json")

        parsed_response = LastFM._download_url(request_url)

        if parsed_response.get("error"):
            error_code = parsed_response["error"]
            error_message = parsed_response["message"]
            raise Exception(error_message)
    
        else:
            track_list = []
            for track in parsed_response["lovedtracks"]["track"]:
                track_artist = track["artist"]["name"]
                track_name = track["name"]
                track_date = datetime.fromtimestamp(int(track["date"]["uts"])).strftime('%m/%d/%Y') 
                track_list.append(f"Artist: {track_artist}, Track: {track_name}, Loved on: {track_date}")

            self.tracks = track_list


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