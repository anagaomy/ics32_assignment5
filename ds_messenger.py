# ds_messenger.py

# Ana Gao
# gaomy@uci.edu
# 26384258

import json
import socket
import ds_protocol

# server = '168.235.86.101'
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
        self.message = message
        self.recipient = recipient
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.server, port))
                if client is None:
                    print("Error! Fail to connect to the server!")
                    return False
                print("Client succeffully connected to " + f"{self.dsuserver} on {port}")

                join_msg = ds_protocol.join(self.username, self.password)

                send = client.makefile('w')
                recv = client.makefile('r')

                send.write(join_msg + '\r\n')
                send.flush()

                response = recv.readline()
                _type, _msg, _token = ds_protocol.extract_json(response)

                if _type == "error":
                    print(_msg)
                    return False
                
                elif _type == "ok":
                    self.token = _token
                    if self.message and not self.message == '' and not self.message.isspace():
                        directMsg = ds_protocol.direct_message(self.token, self.recipient, self.message)

                        send = client.makefile('w')
                        recv = client.makefile('r')

                        send.write(directMsg + '\r\n')
                        send.flush()

                        MSG = recv.readline()

                        _type_, _msg_, _token_ = ds_protocol.msg_response(MSG)

                        if _type_ == "error":
                            print(_msg_)
                            return False

                        elif _type_ == "ok":
                            print(_msg_)
                            return True
                    
                    else:
                        print("ERROR! INVALID DIRECT MESSAGE! ")
                        return False

        except Exception:
            print("ERROR")
            return False
      
    def retrieve_new(self) -> list:
        # must return a list of DirectMessage objects containing all new messages
        new_msg = []
        pass
    
    def retrieve_all(self) -> list:
        # must return a list of DirectMessage objects containing all messages
        pass
