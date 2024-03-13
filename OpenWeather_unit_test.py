# OpenWeather.py
# Ana Gao
# gaomy@uci.edu

import unittest
from OpenWeather import OpenWeather

class TestWeather(unittest.TestCase):

    def setUp(self):
        self.open_weather = OpenWeather("92697", "US")
        self.open_weather.set_apikey("071481e600ad1194c116a0b9e95d56a8")
        self.open_weather.load_data()

    def test_zipcode(self):
        self.assertEqual(self.open_weather.zipcode, "92697")
        
    def test_ccode (self):
        self.assertEqual(self.open_weather.ccode, "US")

    def test_apikey(self):
        self.assertEqual(self.open_weather.apikey, "071481e600ad1194c116a0b9e95d56a8")

    def test_temperature(self):
        self.assertNotEqual(self.open_weather.temperature, None)

    def test_lat_long(self):
        self.assertNotEqual(self.open_weather.latitude, None)
        self.assertNotEqual(self.open_weather.longitude, None)
    
    def test_description(self):
        self.assertNotEqual(self.open_weather.description, None)

    def test_humidity(self):
        self.assertNotEqual(self.open_weather.humidity, None)

    def test_city(self):
        self.assertEqual(self.open_weather.city, "Irvine")
        

if __name__ == '__main__':
    unittest.main()