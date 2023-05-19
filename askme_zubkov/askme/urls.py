from django.urls import path

from .views import *

urlpatterns = [
    path('', homepage, name='home'),
    path('questions/recent/', recent_questions, name='recent_questions'),
    path('questions/hot/', hot_questions, name='hot_questions'),
    path('questions/<int:question_id>/', question_page, name='question_page'),
    path('questions/tag/<int:tag_id>/', tag_questions, name='tag_questions'),
    path('ask/', ask_question, name="ask"),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('settings/', settings, name='settings')
]
