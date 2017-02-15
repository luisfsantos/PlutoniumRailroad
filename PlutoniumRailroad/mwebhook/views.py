from django.http import HttpResponse
from django.shortcuts import render
import configparser
from mwebhook.messages.builder import Builder
from mwebhook.messages.reader import Reader

config = configparser.ConfigParser()
config.read('messages.ini')
token = config.get('DEBUG', 'access.token')
sender = Builder(token)
reader = Reader()


# Create your views here.
def webhook(request):
    if request.method == 'GET':  # verify token
        if request.GET['hub.verify_token'] == 'GenericToken':
            return HttpResponse(request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
    if request.method == 'POST':
        reader.read(request.POST)
        return HttpResponse(status=200)
