from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def handler(request, subsite): # exactly the same name of the arg
    status = request.GET.get('status')
    print(subsite)
    return HttpResponse(f"{status}, so hello world")

def homepage(request):
    # check authorization then make context dir and handler
    tags = ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7"]
    context = {
        "title" : "AskMe",
        "is_authorized" : True,
        "user_nickname" : "Mr. Pupkins",
        "profile_icon_url" : "askme/img/profile.png",
        "avatar" : "askme/img/avatar.png",
        "questions" : range(20),
        "tags" : tags,
        "tags_len": range(len(tags) - 2),
        "question_content" : "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
    }
    return render(request, 'askme/home.html', context=context) # django finds templates in 'templates' folder, therefore set path from this folder


# request - HttpRequest(query, session info)
# HttpResponse arg (str) - HTML page's content