from django.shortcuts import render
from django.http import HttpResponse, HttpResponsePermanentRedirect, Http404
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.http import require_GET
from .models import *

@require_GET
def homepage(request):
    return HttpResponsePermanentRedirect('/questions/')

@require_GET
def recent_questions(request):
    questions = Question.objects.recently_asked(quantity = 1000)
    page = paginate(request, questions, per_page=20)
    paginator, active_page = page.paginator, page.number
    tags = Question.objects.tags()
    best_members = ["pupkin", "petrov", "terminator", "aligator"]
    context = {
        "is_authorized":
        True,
        "user_nickname":
        "Mr. Pupkins",
        "profile_icon_url":
        "askme/img/profile.png",
        "avatar":
        "askme/img/avatar.png",
        "page":page,
        "paginator":paginator,
        "active_page":active_page,
        "tags":
        tags,
        "best_members":
        best_members
    }
    return render(request, 'askme/index.html', context=context)   # django finds templates in 'templates' folder, therefore set path from this folder
    
@require_GET
def tag_questions(request, tag_name):
    pass

def question_page(request, question_id):
    tags = ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7"]
    best_members = ["pupkin", "petrov", "terminator", "aligator"]
    context = {
        "avatar": "askme/img/avatar.png",
        "question": Question.objects.get(id=question_id),
        "tags": tags,
        "best_members": best_members,
        "answers": range(5)
    }
    return render(request, 'askme/question.html', context=context)


def ask_question(request):
    tags = ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7"]
    best_members = ["pupkin", "petrov", "terminator", "aligator"]
    context = {
        "tags": tags,
        "best_members": best_members
    }

    return render(request, 'askme/ask.html', context=context)


def login(request):
    tags = ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7"]
    best_members = ["pupkin", "petrov", "terminator", "aligator"]
    context = {
        "tags": tags,
        "best_members": best_members
    }

    return render(request, 'askme/login.html', context=context)


def register(request):
    tags = ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7"]
    best_members = ["pupkin", "petrov", "terminator", "aligator"]
    context = {
        "tags": tags,
        "best_members": best_members
    }

    return render(request, 'askme/register.html', context=context)


def settings(request):
    tags = ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7"]
    best_members = ["pupkin", "petrov", "terminator", "aligator"]
    context = {
        "account_name": "Chris Buck",
        "tags": tags,
        "best_members": best_members
    }

    return render(request, 'askme/settings.html', context=context)

def paginate(request, objects, per_page=20):
    try:
        page_num = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404 
    try:
       page_limit = int(request.GET.get('limit', per_page))
    except ValueError:
       page_limit = per_page
    if page_limit > per_page:
       page_limit = per_page
    paginator = Paginator(objects, per_page)
    paginator.base_url='/questions/?page='
    try:
        page = paginator.get_page(page_num)
    except EmptyPage: # Raised when page() is given a valid value but no objects exist on that page
        page = paginator.get_page(paginator.num_pages)
    return page

@require_GET
def some_view():
    pass

# request - HttpRequest(query, session info)
# HttpResponse arg (str) - HTML page's content
