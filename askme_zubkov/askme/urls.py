from django.urls import path

from .views import *

urlpatterns = [
    path('', homepage, name='home'),
    path('question/<int:question_id>/', question_page, name='question_page'),
    path('ask/', ask_question, name="ask question")
]

