# ds_messenger.py

# Ana Gao
# gaomy@uci.edu
# 26384258

import json
import socket
import ds_protocol

server = '168.235.86.101'
port = 3021

class DirectMessage:
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None


class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.token = None
      
    def send(self, message: str, recipient: str) -> bool:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((server, port))
                if client is None:
                    print("Error! Fail to connect to the server!")
                    return False
                print("Client succeffully connected to " + f"{self.dsuserver} on {port}")

                directMsg = ds_protocol.direct_message(self.token, recipient, message)

                send = client.makefile('w')
                recv = client.makefile('r')

                send.write(directMsg + '\r\n')
                send.flush()

                response = recv.readline()

        except Exception:
            print("ERROR")
            return False
      
    def retrieve_new(self) -> list:
        # must return a list of DirectMessage objects containing all new messages
        pass
    
    def retrieve_all(self) -> list:
        # must return a list of DirectMessage objects containing all messages
        pass
