# test_ds_message_protocol.py

# Ana Gao
# gaomy@uci.edu
# 26384258

import unittest
import ds_protocol

class TestDSProtocol(unittest.TestCase):

    def test_direct_message(self):
        msg = ds_protocol.direct_message("12345",
                             "ohhimark",
                             "Hello world!")

        self.assertIsInstance(msg, str)

        self.assertNotEqual(msg, '{"token": "12345", "directmessage": {"entry": "Hello world!", "recipient": "ohhimark"}}')
        
    def test_msg_response(self):
        msg = '{"response": {"type": "ok", "message": "Direct message sent"}}'
        _type, message, token = ds_protocol.msg_response(msg)
        self.assertIsInstance(msg, str)

        self.assertEqual(_type, "ok")
        self.assertEqual(message, "Direct message sent")
        self.assertEqual(token, None)
    
    def test_request_response(self):
        msg = '{"response": {"type": "ok", "messages": [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"}, {"message":"Bzzzzz", "from":"thebeemoviescript", "timestamp":"1603167689.3928561"}]}}'
        response = ds_protocol.request_response(msg)
        self.assertIsInstance(msg, str)

        self.assertEqual(response, {'type': 'ok', 'messages': {'markb': {'msg': 'Hello User 1!', 'timestamp': '1603167689.3928561'}, 'thebeemoviescript': {'msg': 'Bzzzzz', 'timestamp': '1603167689.3928561'}}})

    def test_dm_new(self):
        newMsg = ds_protocol.dm_new('12345')
        self.assertIsInstance(newMsg, str)
        self.assertEqual(newMsg, '{"token": "12345", "directmessage": "new"}')


    def dm_all(self):
        newMsg = ds_protocol.dm_all('12345')
        self.assertIsInstance(newMsg, str)
        self.assertEqual(newMsg, '{"token": "12345", "directmessage": "all"}')


if __name__ == '__main__':
    unittest.main()
