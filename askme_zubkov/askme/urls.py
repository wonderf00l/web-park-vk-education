from django.urls import path

from .views import *

from .url_list import WHITELIST

urlpatterns = [
    path(WHITELIST['home'], homepage, name='home'),
    path(WHITELIST['recent_questions'], recent_questions, name='recent_questions'),
    path(WHITELIST['hot_questions'], hot_questions, name='hot_questions'),
    path(WHITELIST['question_page'], question_page, name='question_page'),
    path(WHITELIST['tag_questions'], tag_questions, name='tag_questions'),
    path(WHITELIST['ask_question'], ask_question, name="ask_question"),
    path(WHITELIST['login'], login, name='login'),
    path(WHITELIST['logout'], logout, name='logout'),
    path(WHITELIST['register'], register, name='register'),
    path(WHITELIST['settings'], settings, name='settings')
]
