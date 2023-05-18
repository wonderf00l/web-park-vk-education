from django.urls import path

from .views import *

urlpatterns = [
    path('', homepage, name='home'),
    path('questions/', recent_questions, name='recent'),
    path('questions/<int:question_id>/', question_page, name='question_page'),
    path('questions/<slug:tag_name>/', tag_questions, name='tag_questions'),
    path('ask/', ask_question, name="ask"),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('settings/', settings, name='settings')
]
