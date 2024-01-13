from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models import Count
from datetime import datetime, timedelta
from django.db.models import Sum


# Like.objects.filter(content_type_id=7).values('object_id').annotate(question_rating=Count('object_id')).order_by('-question_rating')
# [dict['object_id'] for dict in a][:5]
# [Question.objects.get(id=dict['object_id']) for dict in a[:quantity]]


class ProfileManager(models.Manager):
    
    def top_users(self, quantity=10):
        users_with_recent_q_n_a=User.objects.filter(Q(question__publication_date__gte=datetime.now().date() - timedelta(days=90)) 
                                                    & Q(answer__publication_date__gte=datetime.now().date() - timedelta(days=90))).distinct() # без distinct - делает inner_join on author.id = user.id(то есть каждому юзеру ставится в соответствие n-ое число его вопрсоов, но т.к. для n вопросов юзер дублируется n раз, то в сумме будет насчитано полей юзеров столько же, сколько и самих вопросов, т.к. изанчально делает join); далее group_by - при annotate
        
        return users_with_recent_q_n_a.annotate(top=(Count('question') + Count('answer'))).order_by('-top')[:quantity]
        


class QuestionManager(models.Manager):

    def recently_asked(self, quantity=500):
        questions = self.order_by("-id")
        if (not quantity or quantity < 0 or quantity > self.last().id):
            quantity = 500
        return questions[:quantity]

    # def hot(self, question_like_stat):
    #     return [self.get(id=dict['object_id']) for dict in question_like_stat]

    def hot(self, quantity=500):
        return self.annotate(rate_=Sum('rating__reaction', default = 0)).order_by('-rate_')[:quantity] # обращаемся к related(вторичной) модели

    def with_tag(self, tag):
        return self.filter(tag__name=tag)


class LikeManager(models.Manager):
    pass
    # def hot_questions_ids(self, quantity=500):
    #     questions_like_stat = self.filter(content_type_id=7).values('object_id').annotate(
    #         question_rating=Count('object_id')).order_by('-question_rating')[:quantity]
    #     # [{'object_id': '27580', 'question_rating': 26}, {'object_id': '22131', 'question_rating': 25} ... ]
    #     return questions_like_stat


class TagManager(models.Manager):

    def top_tags(self, quantity=10):
        tags_with_recent_questions = self.filter(questions__publication_date__gte=datetime.now().date() - timedelta(days=90)).distinct()
        return tags_with_recent_questions.annotate(top=Count('questions')).order_by('-top')[:quantity]