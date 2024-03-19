# ds_messenger.py

# Ana Gao
# gaomy@uci.edu
# 26384258

import socket
import ds_protocol
import datetime


class DirectMessage:
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None


class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None, port=3021):
        self.dsuserver = dsuserver # 168.235.86.101
        self.username = username
        self.password = password
        self.token = None
        self.port = port
        self.client = None
        self.connect_to_server()
    
    def connect_to_server(self):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.dsuserver, self.port))
            print("Client successfully connected to " + f"{self.dsuserver} on {self.port}")

            join_msg = ds_protocol.join(self.username, self.password)

            send = self.client.makefile('w')
            recv = self.client.makefile('r')

            send.write(join_msg + '\r\n')
            send.flush()

            response = recv.readline()
            _type, _msg, _token = ds_protocol.extract_json(response)

            if _type == "error":
                print(_msg)
            elif _type == "ok":
                self.token = _token

        except Exception:
            print("ERROR")

    def close_connection(self):
        if self.client:
            self.client.close()
      
    def send(self, message: str, recipient: str) -> bool:
        """
        return true if message successfully sent, false if send failed.
        """
        self.message = message
        self.recipient = recipient
        try:
            if not self.client:
                self.connect_to_server()

            if self.message and not self.message == '' and not self.message.isspace():
                directMsg = ds_protocol.direct_message(self.token, self.recipient, self.message)

                send = self.client.makefile('w')
                recv = self.client.makefile('r')

                send.write(directMsg + '\r\n')
                send.flush()

                MSG = recv.readline()

                _type_, _msg_, _token_ = ds_protocol.msg_response(MSG)

                if _type_ == "error":
                    print(_msg_)
                    return False

                elif _type_ == "ok":
                    print(f"{_msg_}: {self.message}")
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
        try:
            if not self.client:
                self.connect_to_server()
            
            directMsgNew = ds_protocol.dm_new(self.token)

            send = self.client.makefile('w')
            recv = self.client.makefile('r')

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
                    timestamp_str = str(_messages[user]['timestamp'])
                    timestamp_int = int(timestamp_str.split('.')[0])
                    directMsg.timestamp = timestamp_int
                    time = datetime.datetime.fromtimestamp(directMsg.timestamp).strftime('%d/%m/%Y, %H:%M:%S')
                    print(f"New Direct Message from {user} is {directMsg.message} on {time}.")
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
        try:
            if not self.client:
                self.connect_to_server()

            directMsgNew = ds_protocol.dm_all(self.token)

            send = self.client.makefile('w')
            recv = self.client.makefile('r')

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
                    timestamp_str = str(_messages[user]['timestamp'])
                    timestamp_int = int(timestamp_str.split('.')[0])
                    directMsg.timestamp = timestamp_int
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

