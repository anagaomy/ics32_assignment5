# test_ds_messenger.py

# Ana Gao
# gaomy@uci.edu
# 26384258

import unittest
import ds_messenger


class TestDSMessenger(unittest.TestCase):

    def test_connection(self):
        dsuserver = '168.235.86.101'
        username = "BLACKPINK"
        password = "2016"
        dm = ds_messenger.DirectMessenger(dsuserver, username, password)

        self.assertEqual(dm.dsuserver, dsuserver)
        self.assertEqual(dm.username, username)
        self.assertEqual(dm.password, password)

    def test_send(self):
        dsuserver = '168.235.86.101'
        username = "BLACKPINK"
        password = "2016"
        dm = ds_messenger.DirectMessenger(dsuserver, username, password)
        message = "Hi"
        recipient = "SOMEONE"
        isSend = dm.send(message, recipient)

        self.assertEqual(dm.message, message)
        self.assertEqual(dm.recipient, recipient)
        self.assertTrue(isSend)

    def test_retrieve_new(self):
        dsuserver = '168.235.86.101'
        username = "BLACKPINK"
        password = "2016"
        dm = ds_messenger.DirectMessenger(dsuserver, username, password)
        msg_new = dm.retrieve_new()
        self.assertNotEqual(msg_new, [
            {
                "BLACKPINK": [
                    {
                        "message": "Jin",
                        "timestamp": 1603167719.3928561
                    }
                ]
            }
        ])

    def test_retrieve_all(self):
        dsuserver = '168.235.86.101'
        username = "BLACKPINK"
        password = "2016"
        dm = ds_messenger.DirectMessenger(dsuserver, username, password)
        msg_all = dm.retrieve_all()
        self.assertNotEqual(msg_all, [])


if __name__ == '__main__':
    unittest.main()
