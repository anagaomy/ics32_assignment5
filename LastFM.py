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
import random


class LastFM:

    def __init__(self, user='rj', limit=50, page=1) -> None:
        self.user = user
        self.limit = str(limit)
        self.page = str(page)

    def set_apikey(self, apikey:str) -> None:
        self.apikey = str(apikey)

    def _download_url(self, url_to_download: str) -> dict:
        response = None
        r_obj = None

        try:
            response = urllib.request.urlopen(url_to_download)
            response_body = response.read()
            response_body = response_body.decode(encoding='utf-8')
            r_obj = json.loads(response_body)

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

    def load_data(self) -> None:
        url_to_download = str("http://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user=" +
                          self.user + "&api_key=" + self.apikey + "&limit=" +
                          self.limit + "&page=" + self.page + "&format=json")

        r_obj = LastFM._download_url(self, url_to_download)

        if r_obj.get("error"):
            error_code = r_obj["error"]
            error_message = r_obj["message"]
            raise Exception(error_message)
    
        else:
            track_list = []
            date_list = []
            artist_list = []
            name_list = []
            for track in r_obj["lovedtracks"]["track"]:
                track_artist = track["artist"]["name"]
                track_name = track["name"]
                track_date = datetime.fromtimestamp(int(track["date"]["uts"])).strftime('%m/%d/%Y')

                artist_list.append(track_artist)
                name_list.append(track_name)
                date_list.append(track_date)
                track_list.append(f"Artist: {track_artist}, Track: {track_name}, Loved on: {track_date}")

            self.date = date_list
            self.artist = artist_list
            self.name = name_list
            self.tracks = track_list

    def transclude(self, message: str) -> str:
        keyword = '@lastfm'
        if message.find(keyword) != -1:
            msg_split = message.split(keyword)
            index = random.randint(0, int(self.limit)-1)
            transclude_weather = self.name[index]
            new_message = msg_split[0] + transclude_weather + msg_split[1]
        return new_message


# def main() -> None:
    # username = "rj"
    # apikey = "e05db7fa6efe7323ede21ee2e48c88f5"
    # url_to_download = str("http://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user=" +
                          #username + "&api_key=" + apikey + "&limit=" +
                          #lastFM.limit + "&page=" + lastFM.page + "&format=json")

# if __name__ == '__main__':
    # main()