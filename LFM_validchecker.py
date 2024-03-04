from LastFM import LastFM
import json


username = "rj"
apikey = "e05db7fa6efe7323ede21ee2e48c88f5"


lastFM = LastFM(username)
lastFM.set_apikey(apikey)
lastFM.set_limit()
lastFM.set_page()


dict = lastFM.load_data()

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