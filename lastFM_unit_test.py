# lastFM_unit_test.py

# Ana Gao
# 26384258
# 26384258

import unittest
from LastFM import LastFM

class TestLastFM(unittest.TestCase):
    # Test the set_apikey method
    def test_set_apikey(self):
        # Create a LastFM object
        lastFM = LastFM()
        # Set the apikey
        lastFM.set_apikey("testkey")
        # Check if the apikey is set correctly
        self.assertEqual(lastFM.apikey, "testkey")

    # Test the load_data method
    def test_load_data(self):
        # Create a LastFM object
        lastFM = LastFM("rj", 3, 1)
        # Set the apikey
        lastFM.set_apikey("e05db7fa6efe7323ede21ee2e48c88f5")
        # Load the data
        lastFM.load_data()
        # Check if the data is loaded correctly
        self.assertEqual(len(lastFM.tracks), 3)

    # Test the transclude method
    def test_transclude(self):
        # Create a LastFM object
        lastFM = LastFM("rj")
        # Set the apikey
        lastFM.set_apikey("e05db7fa6efe7323ede21ee2e48c88f5")
        # Load the data
        lastFM.load_data()
        # Set a test message
        msg = "I am listening to @lastfm."
        # Transclude the message
        new_msg = lastFM.transclude(msg)
        # Check if the transcluded message contains the correct song name
        self.assertNotEqual(lastFM.name[0], new_msg)

if __name__ == '__main__':
    unittest.main()
