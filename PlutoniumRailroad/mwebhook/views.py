import threading

from django.http import HttpResponse
from django.shortcuts import render
import configparser
from mwebhook.messages.builder import Builder
from mwebhook.messages.reader import Reader
from django.views.decorators.csrf import csrf_exempt
from google.url_api import UrlShortner
import re

config = configparser.ConfigParser()
config.read('mwebhook/messages.ini')
token = config.get('DEBUG', 'access.token')
sender = Builder(token)
reader = Reader()
url_api = UrlShortner(config.get('DEBUG', 'shortner.api'))

# Create your views here.
@csrf_exempt
def webhook(request):
    if request.method == 'GET':  # verify token
        if request.GET['hub.verify_token'] == 'GenericToken':
            return HttpResponse(request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
    if request.method == 'POST':
        t = threading.Thread(target=proccess_message, args=[request.body.decode('utf-8')])
        # We want the program to wait on this thread before shutting down.
        t.setDaemon(False)
        t.start()
        return HttpResponse(status=200)


def proccess_message(incoming):
    print(incoming)
    print("\n")
    msg = reader.read(incoming)
    for facebookmsg in msg['entry'][0]['messaging']:
        urls = re.findall(r'(https?://[^\s]+)', facebookmsg.message)
        if urls:
            shorts = []
            for url in urls:
                shorts.append(url_api.shortenUrl(url))
            message = "You had some urls ({0}) in your message, I shortened them for you:\n {1}".format(len(urls), ', '.join(str(short) for short in shorts))
            sender.send_message(facebookmsg.user_id, message)
        else:
            sender.send_message(facebookmsg.user_id, facebookmsg.message)
