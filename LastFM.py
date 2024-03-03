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

    def __init__(self, apikey):
        self.apikey = apikey

    def set_user(self, user):
        self.user = user

    def set_limit(self, limit=50):
        self.limit = limit
    
    def set_page(self, page=1):
        self.page = page

    def load_lovedtracks(self):
        request_url = str("http://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user="
                          + self.user + "&api_key=" + self.apikey + "&limit=" +
                          self.limit + "&page=" + self.page + "&format=json")

        try:
            response = urllib.request.urlopen(request_url)
            response_body = response.read()
            response_body = response_body.decode(encoding='utf-8')
            parsed_response = json.loads(response_body)
            if parsed_response.get("error"):
                error_code = parsed_response["error"]
                if error_code == 10:
                    raise Exception("Invalid API key. Check validity and try again.")
                elif error_code == 6:
                    raise Exception("Invalid parameters. Make sure all required parameters are included.")
                else:
                    raise Exception("An error has occurred. Please try again later.")
            
            else:
                track_list = []
                for track in parsed_response["lovedtracks"]["track"]:
                    track_artist = track["artist"]["name"]
                    track_name = track["name"]
                    track_date = datetime.fromtimestamp(int(track["date"]["uts"])).strftime('%m/%d/%Y') 
                    track_list.append(f"'{track_name}' by '{track_artist}' on {track_date}")

                self.tracks = track_list

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