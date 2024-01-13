from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .managers import *
from django.db.models import Sum
# from django.db.models.signals import post_init


class Question(models.Model):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     current_user = None

    # current_user = None либо атрибут класса --> переменная, разделяемая всеми инстансами --> при каждом запросе от любого из юзеров она будет перезаписываться
    # альтернатива: проставлять атрибут явно у ИНСТАНСОВ, либо же формировать массив реакций и прокидывать в контекст

    objects = QuestionManager()

    title = models.CharField(max_length=255, blank=False, null=False, unique=True)
    content = models.TextField(blank=False, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = GenericRelation("Like", related_query_name="likes")
    # rating = models.IntegerField(blank=False, null=False, default=0)
    publication_date = models.DateTimeField(auto_now_add=True)

    # tag in url as slug
    # newest_quantity in get parameters

    @property
    def tags(self):
        return self.tag_set.all()
    
    @property
    def answers(self):
        return self.answer_set.all()

    @property
    def answers_quantity(self):
        return self.answer_set.count()
    
    @property
    def rate(self):
        # return Question.objects.aggregate(Sum('like__reaction')) on field 'like'
        return self.rating.aggregate(Sum('reaction'))['reaction__sum'] or 0

    current_user = None

    # @property
    # def user_reaction(self, author_=[None]):
    #     author_[0] = self.current_user
    #     try:
    #         return self.rating.get(author=author_[0]).reaction # -1 0 1
    #     except Like.DoesNotExist:
    #         return 0

    def get_url(self):
        return reverse('question_page', kwargs={'question_id':self.id})

    def __str__(self):
        return self.title

# def add_curr_user_to_question(user, **kwargs):
#     print(kwargs)
#     instance = kwargs.get('instance')
#     instance.current_user = user

# post_init.connect(add_curr_user_to_question, Question)


class Answer(models.Model):

    current_user = None

    content = models.TextField(blank=False, null=False, max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = GenericRelation("Like", related_query_name="likes")
    is_correct = models.BooleanField(blank=False, null=False, default=False)
    publication_date = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    @property
    def rate(self):
        return self.rating.aggregate(Sum('reaction'))['reaction__sum'] or 0

    # @property
    # def user_reaction(self, author_=current_user):
    #     try:
    #         react = self.rating.get(author=author_).reaction # -1 0 1
    #         return react
    #     except Like.DoesNotExist:
    #         return 0

    def __str__(self):
        return self.content


class Tag(models.Model):

    objects = TagManager()

    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    questions = models.ManyToManyField(Question)

    def get_questions(self):
        return self.questions.all()

    def get_url(self):
        return reverse('tag_questions', kwargs={'tag_id':self.id})

    def __str__(self):
        return self.name


class Profile(models.Model):

    objects = ProfileManager()

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/%Y/%m/%d/", blank=True, null=True, default='default_avatar.png') # default относительно media/ folder(MEDIA_URL)

    def __str__(self):
        return self.user.get_username()
    
    # def question_reaction(self, question_id):
    #     return self.user.question_set.all()[question_id]
    
    # def answer_reaction(self, answer_id):
    #     return self.user.answer_set.all()[answer_id]

class Like(models.Model):

    objects = LikeManager()

    class Meta:
        unique_together = ['author', 'content_type', 'object_id']

    LIKE_CHOICES = [
        (1, "like"),
        (-1, "dislike")
    ]

    reaction = models.SmallIntegerField(choices=LIKE_CHOICES, blank=False, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.RESTRICT)
    object_id = models.PositiveIntegerField() # POSITIVE INTEGER

    content_object = GenericForeignKey("content_type", "object_id")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content_type} - {self.object_id} -  {self.reaction}"
