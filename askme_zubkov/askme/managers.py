from django.db import models
from django.contrib.auth.models import User
from .models import *
from django.db.models import Count
from django.core.exceptions import EmptyResultSet
import datetime



class ProfileManager(models.Manager):
    def reset_rating(self):
        pass # check with auth

class QuestionManager(models.Manager):

    def tags(self):
        return self.tag_set.all()
    
    def answers(self):
        return self.answers_set.all()

    def recently_asked(self, quantity=500):
        questions = self.order_by("-id") 
        if (not quantity or quantity < 0 or quantity > self.last().id):
            quantity = 500
        return questions[:quantity]
    
    def hot(self, quantity=500):
        hot_questions = Question.objects.annotate(likes=Count(('likes'))).order_by('-likes')
        if (not quantity or quantity < 0 or quantity > self.last().id):
            quantity = 500
        return hot_questions[:quantity]

    def with_tag(self, tag):
        return self.filter(tag__name=tag)
         
        