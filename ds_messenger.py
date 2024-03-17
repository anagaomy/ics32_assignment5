# ds_messenger.py

# Ana Gao
# gaomy@uci.edu
# 26384258

import socket
import ds_protocol
import datetime
# server = '168.235.86.101'


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
        """
        return true if message successfully sent, false if send failed.
        """
        self.message = message
        self.recipient = recipient
        port = 3021

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.dsuserver, port))
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
        """
        return a list of DirectMessage objects containing all new messages
        """
        new_msg = []
        port = 3021

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.dsuserver, port))
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
                    directMsgNew = ds_protocol.dm_new(self.token)

                    send = client.makefile('w')
                    recv = client.makefile('r')

                    send.write(directMsgNew + '\r\n')
                    send.flush()

                    MSG = recv.readline()
                    dm_dict = ds_protocol.request_response(MSG)
                    _type = dm_dict['type']
                    _messages = dm_dict['messages']

                    if _type == "ok":
                        for user in _messages:
                            directMsg = DirectMessage()
                            directMsg.recipient = user
                            directMsg.message = _messages[user]['msg']
                            directMsg.timestamp = _messages[user]['timestamp']
                            time = datetime.datetime.fromtimestamp(directMsg.timestamp).strftime('%d/%m/%Y, %H:%M:%S')
                            print(f"New Direct Message for {user} is {directMsg.message} on {time}.")
                            new_msg.append(directMsg)
                        return new_msg

                    else:
                        print("ERROR")
                        return new_msg

        except Exception:
            print("Something wrong with the server")
            return new_msg

    def retrieve_all(self) -> list:
        """
        return a list of DirectMessage objects containing all messages
        """
        all_msg = []
        port = 3021

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.dsuserver, port))
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
                    directMsgNew = ds_protocol.dm_all(self.token)

                    send = client.makefile('w')
                    recv = client.makefile('r')

                    send.write(directMsgNew + '\r\n')
                    send.flush()

                    MSG = recv.readline()
                    dm_dict = ds_protocol.request_response(MSG)
                    _type = dm_dict['type']
                    _messages = dm_dict['messages']

                    if _type == "ok":
                        for user in _messages:
                            directMsg = DirectMessage()
                            directMsg.recipient = user
                            directMsg.message = _messages[user]['msg']
                            directMsg.timestamp = _messages[user]['timestamp']
                            time = datetime.datetime.fromtimestamp(directMsg.timestamp).strftime('%d/%m/%Y, %H:%M:%S')
                            print(f"Direct Message for {user} is {directMsg.message} on {time}.")
                            all_msg.append(directMsg)
                        return all_msg
    
                    else:
                        print("ERROR")
                        return all_msg

        except Exception:
            print("Something wrong with the server")
            return all_msg


if __name__ == "__main__":
    dsuserver = '168.235.86.101'
    username = "BLACKPINK"
    password = "2016"
    message = "Hi"
    recipient = "BTS"
    DM = DirectMessenger(dsuserver, username, password)
    DM.send(message, recipient)
    msg_all = DM.retrieve_all()
    print(msg_all)
    msg_new = DM.retrieve_new()
    print(msg_new)

