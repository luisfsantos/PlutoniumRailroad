from django.http import HttpResponse
from django.shortcuts import render
import configparser
from mwebhook.messages.builder import Builder
from mwebhook.messages.reader import Reader
from django.views.decorators.csrf import csrf_exempt

config = configparser.ConfigParser()
config.read('mwebhook/messages.ini')
token = config.get('DEBUG', 'access.token')
sender = Builder(token)
reader = Reader()


# Create your views here.
@csrf_exempt
def webhook(request):
    if request.method == 'GET':  # verify token
        if request.GET['hub.verify_token'] == 'GenericToken':
            return HttpResponse(request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
    if request.method == 'POST':
        print(request.body.decode('utf-8'))
        print("\n")
        #msg = reader.read(request.body.decode('utf-8'))
        #for facebookmsg in msg['entry'][0]['messaging']:
        #    sender.send_message(facebookmsg.user_id, facebookmsg.message)
        return HttpResponse(status=200)
