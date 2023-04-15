from django.shortcuts import render
from django.http import HttpResponse

def init_handler(request):
    return HttpResponse('INITIAL')