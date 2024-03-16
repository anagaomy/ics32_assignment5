# test_ds_message_protocol.py

# Ana Gao
# gaomy@uci.edu
# 26384258

import unittest
from ds_protocol import extract_json, direct_message

class TestDirectMessageProtocol(unittest.TestCase):

    # Test
    def test_extract_message_1(self):
        json_string = '{"response": {"type": "ok", "can_read": true}}'
        dtype, msg = extract_json(json_string)
        self.assertIsInstance(dtype, str)
        self.assertIsInstance(msg, str)

    # Test direct message
    def test_dm_protocol_1(self):
        # Create a test message
        msg = direct_message("user_token",
                             "some_recipient",
                             "Hello world")

        # Make sure it is a string
        self.assertIsInstance(msg, str)

        # Test that the string matches your expected result
        self.assertEqual(msg, '{"token": "user_token", "directmessage": {"message": "Hello world", "recipient": "some_recipient", "timestamp": "1604552158.788"}}')