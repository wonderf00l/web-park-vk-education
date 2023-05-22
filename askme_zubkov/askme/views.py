from .url_list import WHITELIST
from django.shortcuts import render, redirect
from django.http import HttpResponsePermanentRedirect, Http404
from django.db import IntegrityError
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.http import require_GET
from .models import *
from .forms import *

@require_GET
def homepage(request):
    return HttpResponsePermanentRedirect('/questions/recent/')

def questions_list(request, processor,url_infix):
    questions = processor(quantity = 1000)
    page = paginate(request, questions, per_page=20)
    paginator, active_page = page.paginator, page.number
    paginator.base_url=f'/questions/' + url_infix + '?page='
    pop_tags = ['tag1', 'tag2', 'tag3', 'tag4', 'tag5', 'tag6', 'tag7']
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
        "pop_tags":
        pop_tags,
        "best_members":
        best_members
    }
    return context

@require_GET
def recent_questions(request):
    return render(request, 'askme/index.html', context=questions_list(request, Question.objects.recently_asked, 'recent/'))   # django finds templates in 'templates' folder, therefore set path from this folder

@require_GET
def hot_questions(request):
    return render(request, 'askme/index.html', context=questions_list(request, Question.objects.hot, 'hot/'))


@require_GET
def tag_questions(request, tag_id):
    tag = Tag.objects.get(id=tag_id) 
    questions = tag.get_questions()
    page = paginate(request, questions, per_page=20)
    paginator, active_page = page.paginator, page.number
    paginator.base_url='/questions/tag/' + str(tag_id)
    pop_tags = ['tag1', 'tag2', 'tag3', 'tag4', 'tag5', 'tag6', 'tag7']
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
        "pop_tags":
        pop_tags,
        "best_members":
        best_members,
        "tag":tag,
        "questions": questions
    }
    return render(request, 'askme/tag_questions.html', context=context)

def question_page(request, question_id):
    question = Question.objects.get(id=question_id)
    answers = question.answers
    page = paginate(request, answers, per_page=30)
    paginator, active_page = page.paginator, page.number
    paginator.base_url = '/questions/' + str(question_id)
    pop_tags = ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7"]
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
        "pop_tags":
        pop_tags,
        "best_members":
        best_members,
        "tag":pop_tags,
        "question":question,
        "answers": answers
    }
    return render(request, 'askme/question.html', context=context)


def ask_question(request): # questionfrom.save() override

    tags = ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7"]
    best_members = ["pupkin", "petrov", "terminator", "aligator"]

    if request.method == 'POST':
        question_form = AddQuestionForm(request.POST)
        tag_form = AddTagForm(request.POST) # title tag in form
        if question_form.is_valid() and tag_form.is_valid():
            new_question = question_form.save()
            try:
                tag_attrs = tag_form.cleaned_data.update({'author_id': new_question.id})
                Tag.objects.create(**tag_form.cleaned_data)
                return redirect(reverse('question_page', kwargs={'question_id':new_question.id}))
            except ValueError:
                print("ALREADY PRESENTED")
            # try: add tag -- exc: IntegrityError: already presented
    elif request.method == 'GET':
        question_form = AddQuestionForm()
        tag_form = AddTagForm()
    # check data for unuqueness
    context = {
        "tags": tags,
        "best_members": best_members,
        "question_form":question_form,
        "tag_form":tag_form
    }

    # берем данные юзера - смотрим id сессии -- получаем логин -- идем по логину в бд и вытаскиваем оттуда инстанс юзера -- потом его присвоем полю author нового вопроса, тегу присвоим новый созданный вопрос

    return render(request, 'askme/ask.html', context=context)

def register(request):

    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST)
        if register_form.is_valid():
            user_ = register_form.save()
            Profile.objects.create(avatar=register_form.cleaned_data.get('avatar'), user=user_)
            login(request, user_)
            return redirect('home')
    else:
        register_form = UserRegisterForm()

    tags = ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7"]
    best_members = ["pupkin", "petrov", "terminator", "aligator"]
    context = {
        "tags": tags,
        "best_members": best_members,
        "register_form": register_form
    }

    return render(request, 'askme/register.html', context=context)

def login(request): # check 'continue'

    if request.method == 'POST':
        redirect_path = request.GET.get('continue') if request.GET.get('continue') in WHITELIST.values() else WHITELIST['home']
        print(redirect_path)
        login_form = AuthenticationForm(request.POST) 
        if login_form.is_valid(): # authenticate() inside clean() which is triggered by is_valid() (or form.errors)
            login(request, login_form.get_user()) # session creation inside this method
            print(login_form.get_user().__dict__)
            return redirect(redirect_path)
        print('INVALID LOGIN')
    elif request.method == 'GET':
        login_form = AuthenticationForm()

    tags = ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7"]
    best_members = ["pupkin", "petrov", "terminator", "aligator"]
    context = {
        "tags": tags,
        "best_members": best_members,
        "login_form": login_form
    }

    return render(request, 'askme/login.html', context=context)


    tags = ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7"]
    best_members = ["pupkin", "petrov", "terminator", "aligator"]
    context = {
        "tags": tags,
        "best_members": best_members
    }
    print(request.POST)
    return render(request, 'askme/login.html', context=context)


def settings(request):
    tags = ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7"]
    best_members = ["pupkin", "petrov", "terminator", "aligator"]
    context = {
        "account_name": "Chris Buck",
        "tags": tags,
        "best_members": best_members
    }
    Question.objects.annotate

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
    try:
        page = paginator.get_page(page_num)
    except EmptyPage: # Raised when page() is given a valid value but no objects exist on that page
        page = paginator.get_page(paginator.num_pages)
    return page

def some_view(request):
    if request.method == 'POST':
        form = TestForm(request.POST, request.FILES) # ecntype in html form
        if form.is_valid():
            try:
                Question.objects.create(**form.cleaned_data) # form.save() without try-exc --- for modelForm
                return redirect('recent_questions')
            except:
                form.add_error(None, 'Error!') # for whole form -- form.non_field_errors
    elif request.method == 'GET':
        form = TestForm()
    return render(request, '', context={'form':form})

# request - HttpRequest(query, session info)
# HttpResponse arg (str) - HTML page's content
