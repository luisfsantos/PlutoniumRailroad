import json

class FacebookMessage(object):

    def __init__(self, user_id, message):
        self.user_id = user_id
        self.message = message

class Reader(object):

    def __init__(self):
        self.version = 2.6

    @staticmethod
    def as_facebook_message(message):
        if "message" in message:
            return FacebookMessage(message['sender']['id'], message['message']['text'])
        return message

    def read(self, payload):
        data = json.loads(payload, object_hook=Reader.as_facebook_message)
        return data

