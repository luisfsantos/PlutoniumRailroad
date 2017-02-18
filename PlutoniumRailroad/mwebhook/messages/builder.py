import json
import requests


class Builder(object):
    RECIPIENT = "recipient"
    ID = "id"
    MESSAGE = "message"
    TEXT = "text"
    URL = "https://graph.facebook.com/v2.6/me/messages?access_token="

    def __init__(self, access_token):
        self.token = access_token

    def build_json_payload(self, data, user_id):
        data[self.RECIPIENT] = {
            self.ID: user_id
        }
        return json.dumps(data)

    def send_payload(self, payload):
        send_url = self.URL + self.token
        headers = {'content-type': 'application/json'}
        response = requests.post(send_url, data=payload, headers=headers)
        return response

    def send(self, data, user_id):
        json_payload = self.build_json_payload(data, user_id)
        return self.send_payload(json_payload)

    def send_message(self, user_id, message):
        data = dict()
        data[self.MESSAGE] = {
            self.TEXT: str(message)
        }
        self.send(data, user_id)
