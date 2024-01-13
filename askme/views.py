from django.core.cache import cache
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponsePermanentRedirect, Http404, HttpResponseBadRequest
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.core.exceptions import BadRequest
from .models import *
from .forms import *

def default_context(*args, **kwargs):
    # pop_tags = ['tag1', 'tag2', 'tag3', 'tag4', 'tag5', 'tag6', 'tag7']
    # best_members = ['vasya', 'terminator', 'aligator', 'pupkin', 'puma']
    # return {
    #     'pop_tags': pop_tags,
    #     'best_members': best_members 
    # }
    return {'pop_tags': cache.get('top_tags'),
            'best_members': cache.get('top_users')}
    
def get_vote_by_user(model_inst, curr_user):
    try:
        return model_inst.rating.get(author=curr_user).reaction # -1 0 1
    except Like.DoesNotExist:
        return 0
    
def add_reaction_attr(model_inst, curr_user):
    if curr_user.is_authenticated:
        model_inst.current_reaction = get_vote_by_user(model_inst, curr_user)
    else:
        model_inst.current_reaction = None

@require_GET
def homepage(request):
    return HttpResponsePermanentRedirect('/questions/recent/')

def questions_list(request, processor, url_infix):
    Question.current_user = request.user
    questions = processor(quantity = 1000)
    [add_reaction_attr(question, request.user) for question in questions]
    page = paginate(request, questions, per_page=20)
    paginator, active_page = page.paginator, page.number
    paginator.base_url=f'/questions/' + url_infix + '?page='
    return dict(default_context(), **{
        "user": request.user,
        "page":page,
        "paginator":paginator,
        "active_page":active_page,
    })

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
    [add_reaction_attr(question, request.user) for question in questions]
    page = paginate(request, questions, per_page=20)
    paginator, active_page = page.paginator, page.number
    paginator.base_url='/questions/tag/' + str(tag_id)
    return render(request, 'askme/tag_questions.html', context=dict(default_context(), **{
        "page":page,
        "paginator":paginator,
        "active_page":active_page,
        "tag":tag,
        "questions": questions
    }))

@require_http_methods(['GET', 'POST'])
def question_page(request, question_id):
    Question.current_user = request.user

    if request.method == 'POST':
        answer_form = AddAnswerForm(data=request.POST)
        if answer_form.is_valid():
            question = Question.objects.get(id=question_id)
            answer_form.save(question, request.user)
            return redirect(request.path) # /questions/<question_id>

    answer_form = AddAnswerForm()
    question = Question.objects.get(id=question_id)
    add_reaction_attr(question, request.user)
    answers = question.answers
    [add_reaction_attr(answer, request.user) for answer in answers]
    page = paginate(request, answers, per_page=30)
    paginator, active_page = page.paginator, page.number
    paginator.base_url = '/questions/' + str(question_id)
    return render(request, 'askme/question.html', context=dict(default_context(), **{
        "page":page,
        "paginator":paginator,
        "active_page":active_page,
        "question":question,
        "answers": answers,
        "answer_form": answer_form
    }))

@require_http_methods(['GET', 'POST'])
@login_required(redirect_field_name='continue')
def ask_question(request):

    if request.method == 'POST':
        question_form = AddQuestionForm(request.POST, request.user)
        if question_form.is_valid():
            new_question = question_form.save(request.user)
            return redirect(reverse('question_page', kwargs={'question_id':new_question.id}))
    elif request.method == 'GET':
        question_form = AddQuestionForm()

    return render(request, 'askme/ask.html', context=dict(default_context(), **{
        "question_form":question_form,
    }))

@require_http_methods(['GET', 'POST'])
def register(request):

    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            user_ = register_form.save()
            # messages.success(request, 'Successful register')
            auth.login(request, user_)
            return redirect('home')
    else:
        register_form = UserRegisterForm()

    return render(request, 'askme/register.html', context=dict(default_context(), **{
        "register_form": register_form
    }))

@require_http_methods(['GET', 'POST'])
def login(request): # check 'continue'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'GET':
        login.continue_url = request.GET.get('continue')
        login_form = AuthenticationForm()
    elif request.method == 'POST':
        redirect_path = login.continue_url if login.continue_url and login.continue_url[0] == '/' else 'home' # проверка урла, если пришли из login_required, в случае самостоятельной авторизации get параметр - None('') --> выпадет дефолтный home('')
        # alternate: проверка, что перенаправление относительно домена, т.е. login.url[0] == '/'
        # кеширование continue: через cache.set(contunie_url) -- cache.get() -- cache.delete()
        login_form = AuthenticationForm(request, request.POST) # request.POST only if custom subclass
        if login_form.is_valid(): # authenticate() inside clean() which is triggered by is_valid() (or form.errors)
            auth.login(request, login_form.get_user()) # session creation inside this method
            login.continue_url = ''
            return redirect(redirect_path)
        
    return render(request, 'askme/login.html', context=dict(default_context(), **{
        "login_form": login_form
    }))

@require_http_methods(['GET', 'POST'])
@login_required(redirect_field_name='continue') # .../&continue=урл страницы, куда login_required
def logout(request):
    auth.logout(request)
    # messages.success(request, "Log out successfully")
    return redirect('recent_questions')

@require_http_methods(['GET', 'POST'])
@login_required(redirect_field_name='continue')
def settings(request):

    if request.method == 'POST':
        settings_form = UserSettingsForm(data=request.POST, files=request.FILES, instance=request.user)
        if settings_form.is_valid():
            settings_form.save()
            return redirect('settings')
    elif request.method == 'GET':
        settings_form = UserSettingsForm(initial=model_to_dict(request.user))

    return render(request, 'askme/settings.html', context=dict(default_context(), **{
        "settings_form": settings_form
    }))

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



@require_POST
def question_react(request):
    print(f'BODY:   {request.body}') # POST query parameters in binary representation
    print(f'DICT: {request.POST}') # same represented with QueryDict

    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)

    try:
        question_id = request.POST.get('question_id')
        reaction = int(request.POST.get('reaction'))
        if not question_id or not reaction or reaction not in [-1, 1]:
            raise BadRequest
        question = Question.objects.get(id=question_id)
    except (BadRequest, Question.DoesNotExist):
        return HttpResponseBadRequest()

    add_reaction_attr(question, request.user)
    if question.current_reaction != 0: # обнуление реакции
        Like.objects.filter(author=request.user,
                            content_type=ContentType.objects.get(app_label='askme', model='question'), 
                            object_id=question_id).delete()
        question.current_reaction = 0
    else:
        Like.objects.create(reaction=reaction, 
                            author=request.user, 
                            content_type=ContentType.objects.get(app_label='askme', model='question'),
                            object_id = question_id)
        question.current_reaction = reaction

    # Question.current_user = request.user # authorized, so will always get session user
    # print(Question.current_user.id) # none by default --> forced to write method call inside template (or list of reactions - bad)
    # Question.current_reaction = request.user
    return JsonResponse({
        'status': 'ok',
        'user_rating': question.current_reaction, # -1 0 1
        'total_rating': question.rate
    })

@require_POST
def answer_react(request):

    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)

    try:
        answer_id = request.POST.get('answer_id')
        reaction = int(request.POST.get('reaction'))
        if not answer_id or not reaction or reaction not in [-1, 1]:
            raise BadRequest
        answer = Answer.objects.get(id=answer_id)
    except (BadRequest, Answer.DoesNotExist):
        return HttpResponseBadRequest()

    add_reaction_attr(answer, request.user)
    if answer.current_reaction != 0: # обнуление реакции
        Like.objects.filter(author=request.user,
                            content_type=ContentType.objects.get(app_label='askme', model='answer'), 
                            object_id=answer_id).delete()
        answer.current_reaction = 0
    else:
        Like.objects.create(reaction=reaction, 
                            author=request.user, 
                            content_type=ContentType.objects.get(app_label='askme', model='answer'),
                            object_id = answer_id)
        answer.current_reaction = reaction

    return JsonResponse({
        'status': 'ok',
        'user_rating': answer.current_reaction, # -1 0 1
        'total_rating': answer.rate
    })

@require_POST
def check_answer(request):
    
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)

    try:
        answer_id = request.POST.get('answer_id')
        question_id = request.POST.get('question_id')
        if not answer_id or not question_id:
            raise BadRequest
        answer = Answer.objects.get(id=answer_id, question_id=question_id)
    except (BadRequest, Answer.DoesNotExist):
        return HttpResponseBadRequest()
    
    answer.is_correct = not answer.is_correct
    answer.save()

    return JsonResponse({
        'status': 'ok',
        'is_correct': answer.is_correct,
    })
    # снятие чекбокса - отпрвка is_correct = -1 --> снятие/простановка бокса - 2 разных события

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

# if request.user.is_authenticated:
    # inst = QuestionWrapper(request.user)
# else: default __init__ while calling super().__init__ from Question instance, so current_user is None
# хотя т.к тянем этот атрибут только в q.user_recation, можно писать анонимного юзера в случае not authenticated