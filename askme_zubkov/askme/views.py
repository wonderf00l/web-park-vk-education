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
    best_members = ["pupkin", "petrov", "terminator", "aligator"]
    context = {
        "title" : "AskMe",
        "is_authorized" : True,
        "user_nickname" : "Mr. Pupkins",
        "profile_icon_url" : "askme/img/profile.png",
        "avatar" : "askme/img/avatar.png",
        "questions" : range(20),
        "tags" : tags,
        "tags_len": range(len(tags) - 2),
        "best_members" : best_members,
        "question_content" : "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
    }
    return render(request, 'askme/index.html', context=context) # django finds templates in 'templates' folder, therefore set path from this folder

def question_page(request, question_id):
    tags = ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7"]
    best_members = ["pupkin", "petrov", "terminator", "aligator"]
    context = {
        "title" : "AskMe",
        "avatar" : "askme/img/avatar.png",
        "questions" : range(20),
        "tags" : tags,
        "tags_len": range(len(tags) - 2),
        "best_members" : best_members,
        "question_content" : "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
        "answer_content" : "JUST DO IT JUST DO IT JUST DO IT JUST DO IT JUST DO IT JUST DO IT JUST DO IT JUST DO IT JUST DO IT JUST DO IT JUST DO IT JUST DO IT JUST DO IT JUST DO IT JUST DO IT JUST DO IT",
        "answers" : range(5)
    }
    return render(request, 'askme/question.html', context=context)

def ask_question(request):
    tags = ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7"]
    best_members = ["pupkin", "petrov", "terminator", "aligator"]
    context = {
       "title" : "AskMe", 
       "tags" : tags,
        "tags_len": range(len(tags) - 2),
        "best_members" : best_members
    }
    
    return render(request, 'askme/ask.html', context=context) 

def login(request):
    tags = ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7"]
    best_members = ["pupkin", "petrov", "terminator", "aligator"]
    context = {
       "title" : "AskMe", 
       "tags" : tags,
        "tags_len": range(len(tags) - 2),
        "best_members" : best_members
    }
    
    return render(request, 'askme/login.html', context=context) 

# request - HttpRequest(query, session info)
# HttpResponse arg (str) - HTML page's content