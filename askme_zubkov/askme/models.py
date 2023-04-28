from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Question(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False, unique=True)
    content = models.TextField(blank=False, null=False)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    rating = GenericRelation("Assessment", related_query_name="likes")
    # rating = models.IntegerField(blank=False, null=False, default=0)
    publication_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Answer(models.Model):

    # question_states = [
    #     ("CR", "Correct"),
    #     ("NS", "Not stated"),
    # ]

    content = models.TextField(blank=False)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    # rating = models.IntegerField(blank=False, null=False, default=0)
    rating = GenericRelation("Assessment", related_query_name="likes")
    correctness_degree = models.PositiveIntegerField(blank=False, null=False, default=0)
    publication_date = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    question = models.ManyToManyField(Question)

    def __str__(self):
        return self.name


class Profile(models.Model):

    # delattr(AbstractUser, "first_name")
    # delattr(AbstractUser, "last_name")
    # User.first_name = None
    # User.last_name = None
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    avatar = models.ImageField(upload_to="avatars/", unique=True, null=True)

    def __str__(self):
        return self.user.get_username()

class Assessment(models.Model):
    assessment_type_choices = [
        ("like", "like"),
        ("dislike", "dislike")
    ]
    type = models.CharField(max_length=7, choices=assessment_type_choices)
    author = models.ForeignKey(User, on_delete=models.PROTECT)

    content_type = models.ForeignKey(ContentType, on_delete=models.RESTRICT)
    object_id = models.CharField(max_length=50)

    assessment_obj = GenericForeignKey("content_type", "object_id")
    assessment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type}: {self.assessment_obj}"
