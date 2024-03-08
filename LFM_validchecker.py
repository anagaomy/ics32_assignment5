# LFM_validchecker.py

# Ana Gao
# gaomy@uci.edu
# 26384258

from LastFM import LastFM
import json


username = "rj"
apikey = "e05db7fa6efe7323ede21ee2e48c88f5"


lastFM = LastFM(username)
lastFM.set_apikey(apikey)
lastFM.load_data()

url_to_download = str("http://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user=" +
                      username + "&api_key=" + apikey + "&limit=" +
                      lastFM.limit + "&page=" + lastFM.page + "&format=json")

dict = lastFM._download_url(url_to_download)

file_out = open('lastFM.json', "w")
json.dump(dict, file_out, indent=4)
file_out.close()

print(f"Username: {lastFM.user}. \n")

print("--------------------------------------------------")
print(f"Your {lastFM.limit} favorite songs ❤️: ")
print("--------------------------------------------------")
for track in lastFM.tracks:
    print(track)
print("--------------------------------------------------") 

msg = lastFM.transclude("I am listening to @lastfm.")
print(msg)