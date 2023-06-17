from django.urls import path
from django.conf.urls.static import static
from django.conf import settings as settings_

from .views import *

urlpatterns = [
    path('', homepage, name='home'),
    path('questions/recent/', recent_questions, name='recent_questions'),
    path('questions/hot/', hot_questions, name='hot_questions'),
    path('questions/<int:question_id>/', question_page, name='question_page'),
    path('questions/tag/<int:tag_id>/', tag_questions, name='tag_questions'),
    path('ask/', ask_question, name="ask_question"),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('profile/edit/', settings, name='settings'),
    path('question/react/', question_react, name='question_react'),
    path('answer/react/', answer_react, name='answer_react'),
    path('answer/correct/', check_answer, name='check_answer'),
]   

if settings_.DEBUG: # раздача медиа в дебаг-режиме(уже будет доступна по урлу localhost/.../img.png)
    urlpatterns += static(settings_.MEDIA_URL, document_root=settings_.MEDIA_ROOT)