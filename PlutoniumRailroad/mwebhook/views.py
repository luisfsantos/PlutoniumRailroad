from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def webhook(request):
    if request.method == 'GET': #verify token
        if request.GET['hub.verify_token'] == 'GenericToken':
            return HttpResponse(request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')