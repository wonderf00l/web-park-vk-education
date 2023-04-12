from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    status = request.GET.get('status')
    return HttpResponse(f"{status}, so hello world")


# reqest - HttpRequest(query, session info)
# HttpResponse arg (str) - HTML page's content