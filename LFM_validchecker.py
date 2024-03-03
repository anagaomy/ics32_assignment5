from LastFM import LastFM
import json


username = "rj"
apikey = "e05db7fa6efe7323ede21ee2e48c88f5"

lastFM = LastFM(username)
lastFM.set_apikey(apikey)
dict = lastFM.load_data()

file_out = open('lastFM.json', "w")
json.dump(dict, file_out, indent=4)
file_out.close()

print(f"The temperature for {zipcode} is {open_weather.temperature} degrees")
