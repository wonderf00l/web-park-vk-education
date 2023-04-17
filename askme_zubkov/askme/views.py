from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def handler(request, subsite): # exactly the same name of the arg
    status = request.GET.get('status')
    print(subsite)
    return HttpResponse(f"{status}, so hello world")

def homepage(request):
    # check authorization then make context dir and handler
    context = {
        "title" : "AskMe",
        "is_authorized" : True,
        "user_nickname" : "Mr. Pupkins",
        "profile_icon_url" : "askme/img/profile.png",
        "avatar" : "askme/img/avatar.png"
    }
    return render(request, 'askme/home.html', context=context) # django finds templates in 'templates' folder, therefore set path from this folder


# request - HttpRequest(query, session info)
# HttpResponse arg (str) - HTML page's content