from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .managers import QuestionManager, LikeManager
from django.db.models import Sum

class Question(models.Model):

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

    def get_url(self):
        return reverse('question_page', kwargs={'question_id':self.id})

    def __str__(self):
        return self.title


class Answer(models.Model):

    class Meta:
        ordering = ['id']

    content = models.TextField(blank=False, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = GenericRelation("Like", related_query_name="likes")
    correctness_degree = models.SmallIntegerField(blank=False, null=False, default=0)
    publication_date = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    @property
    def rate(self):
        return self.rating.aggregate(Sum('reaction'))['reaction__sum'] or 0

    def __str__(self):
        return self.content


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    questions = models.ManyToManyField(Question)

    def get_questions(self):
        return self.questions.all()

    def get_url(self):
        return reverse('tag_questions', kwargs={'tag_id':self.id})

    def __str__(self):
        return self.name


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/%Y/%m/%d/", blank=True, null=True, default='default_avatar.png') # default относительно media/ folder(MEDIA_URL)

    def __str__(self):
        return self.user.get_username()

class Like(models.Model):

    objects = LikeManager()

    class Meta:
        unique_together = ['author', 'content_type', 'object_id', 'reaction'] # 'reaction' добавляем, т.к. пользователь может поставить лайк, затем дизлайк(при этом поля тип сущности, id сущности и автор в этому случае повторяются, однако реакция уже другая), в суммарном рейтинге это будет учтено

    LIKE_CHOICES = [
        (1, "like"),
        (-1, "dislike")
    ]

    reaction = models.SmallIntegerField(choices=LIKE_CHOICES)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.RESTRICT)
    object_id = models.PositiveIntegerField() # POSITIVE INTEGER

    content_object = GenericForeignKey("content_type", "object_id")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content_type} - {self.object_id} -  {self.reaction}"
