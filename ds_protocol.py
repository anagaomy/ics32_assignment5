# ds_protocol.py

# Ana Gao
# gaomy@uci.edu
# 26384258

import json
from collections import namedtuple
from Profile import Post


RESPONSE = namedtuple('RESPONSE', ['type', 'msg', 'token'])


def extract_json(json_msg: str) -> RESPONSE:
    '''
    Call the json.loads function on a json string
    and convert it to a DataTuple object

    TODO: replace the pseudo placeholder keys with actual DSP protocol keys
    '''
    try:
        json_obj = json.loads(json_msg)
        response = json_obj['response']
        type = response['type']
        msg = response['message']
        token = response['token']
        print("token: ", token)
        return RESPONSE(type, msg, token)

    except json.JSONDecodeError:
        print("Json cannot be decoded.")
        return RESPONSE(type, msg, None)


def join(username, password):
    join_msg = json.dumps({
        "join": {
            "username": username,
            "password": password,
            "token": ""
        }
    })
    return join_msg


def post(token, message):
    new_post = Post(entry=message)
    post_msg = json.dumps({
        "token": token,
        "post": {
            "entry": message,
            "timestamp": new_post.timestamp
        }
    })
    return post_msg


def bio(token, bio):
    new_bio = Post(entry=bio)
    bio_msg = json.dumps({
        "token": token,
        "bio": {
            "entry": bio,
            "timestamp": new_bio.timestamp
        }
    })
    return bio_msg


def msg_response(directMsg: str):
    try:
        json_msg = json.loads(directMsg)
        response = json_msg['response']
        _type = response['type']
        message = response['message']

        # response_dict = {
        #     "type" : _type,
        #     "message": message
        #     }
        # return response_dict

        return RESPONSE(_type, message, None)

    except json.JSONDecodeError:
        print("Json cannot be decoded.")
        return RESPONSE(_type, message, None)


def request_response(directMsg: str):
    try:
        json_msg = json.loads(directMsg)
        response = json_msg['response']
        _type = response['type']
        msg_dict = {}
        for item in json_msg['response']['messages']:
            msg_dict[item['from']] = {
                'msg': item['message'],
                'timestamp': item['timestamp']
                }
        response_dict = {
            "type" : _type,
            "messages": msg_dict
            }
        return response_dict

    except json.JSONDecodeError:
        print("Json cannot be decoded.")
        return


def direct_message(token, recipient, message):
    msg = Post(entry=message)
    directMsg = json.dumps({
        "token": token,
        "directmessage": {
            "entry": message,
            "recipient": recipient,
            "timestamp": msg.timestamp
        }
    })
    return directMsg


def dm_new(token: str):
    directMessageNew = json.dumps({
        "token": token,
        "directmessage": "new"
    })
    return directMessageNew


def dm_all(token: str):
    directMessageAll = json.dumps({
        "token": token,
        "directmessage": "all"
    })
    return directMessageAll
