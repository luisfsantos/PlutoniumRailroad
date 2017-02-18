import requests
import json

class UrlShortner(object):
    url = "https://www.googleapis.com/urlshortener/v1/url?key="

    def __init__(self, token):
        self.token = token

    def shortenUrl(self, url):
        send_url = self.url + self.token
        data = {
            "longUrl": url
        }
        payload = json.dumps(data)
        headers = {'content-type': 'application/json'}
        response = requests.post(send_url, data=payload, headers=headers).json()
        if "id" in response.keys():
            return response["id"]
        else:
            return "Error on shortening url"