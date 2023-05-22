from django.core.management.base import BaseCommand
from askme.models import User, Profile, Question, Answer, Tag, Like
from faker import Faker
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.models import ContentType
from django.db.utils import IntegrityError
from random import randint

# obj_id = randint - without QuierySets - THE MOST EFFICIENT WAY
# get QuierySet -- QuierySet[randint]
# seperate one-operation functions: nested behaviour


class Command(BaseCommand):
    help = "Fill db"
    fake = Faker()

    email_samples = [
        "@yandex.ru",
        "@mail.ru",
        "@gmail.com",
        "@outlook.com",
        "@bmstu.ru",
        "@student.com"
    ]

    img_url_prefix = "static/img/avatars/"

    def add_arguments(self, parser):
        parser.add_argument("ratio", type=int, help="db density coeff")

    # def create_profile(self):
    #     user = User.objects.create(username=self.fake.simple_profile()["username"], email=self.fake.simple_profile()["mail"], password=self.fake.name(), last_login=self.fake.date_time())
    #     return Profile.objects.create(avatar="static/img/avatars", user_id=user)

    def create_profiles(self, profiles_quantity, chunks_quantity=100):

        chunk_size = int(profiles_quantity / chunks_quantity)

        for i in range(chunks_quantity):
            User.objects.bulk_create([
                User(username=AbstractBaseUser.normalize_username(self.fake.unique.company()),
                    email=BaseUserManager.normalize_email(self.fake.unique.company() + self.email_samples[randint(0, len(self.email_samples) - 1)]), password=make_password(self.fake.name(), None, 'md5'), last_login=timezone.now())
                for j in range(chunk_size)
            ])

        offset = 0

        for i in range(chunks_quantity):
            Profile.objects.bulk_create([
                Profile(avatar=self.img_url_prefix + str(offset + j + 1), user_id=offset + j + 1)
                for j in range(chunk_size)
            ])
            offset += chunk_size

    def create_questions(self, questions_quantity, chunks_quantity=100):

        chunk_size = int(questions_quantity / chunks_quantity)

        # profiles = User.objects.all()

        # offset = 0

        profiles_last = Profile.objects.last().id

        for i in range(chunks_quantity):
            Question.objects.bulk_create([
                Question(title=self.fake.unique.catch_phrase(
                ), content=self.fake.text(), author_id=randint(1, profiles_last))
                for j in range(chunk_size)
            ])
            # offset += chunk_size

    def create_answers(self, answers_quantity, chunks_quantity=100):

        chunk_size = int(answers_quantity / chunks_quantity)

        profiles_last = Profile.objects.last().id
        questions_last = Question.objects.last().id

        for i in range(chunks_quantity):

            Answer.objects.bulk_create([
                Answer(content=self.fake.text(), correctness_degree=randint(1, profiles_last), author_id=randint(1, profiles_last),
                    question_id=randint(1, questions_last))
                for j in range(chunk_size)
            ])

    # def create_likes(self, likes_quantity, chunks_quantity=10000):

    #     chunk_size = int(likes_quantity / chunks_quantity)

    #     # types = [
    #     #     "like",
    #     #     "dislike"
    #     # ]

    #     ct_question, ct_answer = ContentType.objects.get_for_model(
    #         Question), ContentType.objects.get_for_model(Answer)
    #     content_types = (ct_question, ct_answer)

    #     profiles_last = User.objects.last().id
    #     questions_last = Question.objects.last().id
    #     answers_last = Answer.objects.last().id

    #     for i in range(chunks_quantity):

    #         likes = list()

    #         for j in range(chunk_size):
    #             content_type_ = content_types[randint(0, len(content_types) - 1)]
    #             obj_id = randint(1, questions_last) if content_type_ == ct_question else randint(
    #                 1, answers_last)
    #             likes.append(Like(reaction=[-1, 1][randint(0, 1)],content_type=content_type_, object_id=obj_id, author_id=randint(1, profiles_last)))

    #         Like.objects.bulk_create(likes, ignore_conflicts=True) # ignore IntegrityError
            
    #         # if (Assessment.objects.last().id and Assessment.objects.last().id == likes_quantity):
    #         #     break

    def create_likes(self, likes_quantity, chunks_quantity=10000):

        chunk_size = int(likes_quantity / chunks_quantity)

        ct_question, ct_answer = ContentType.objects.get_for_model(
            Question), ContentType.objects.get_for_model(Answer)
        content_types = (ct_question, ct_answer)

        profiles_last = User.objects.last().id
        questions_last = Question.objects.last().id
        answers_last = Answer.objects.last().id

        counter = 0

        while(counter != chunks_quantity):

            likes = list()

            for j in range(chunk_size):
                content_type_ = content_types[randint(0, len(content_types) - 1)]
                obj_id = randint(1, questions_last) if content_type_ == ct_question else randint(
                    1, answers_last)
                likes.append(Like(reaction=[-1, 1][randint(0, 1)],content_type=content_type_, object_id=obj_id, author_id=randint(1, profiles_last)))

            try:
                Like.objects.bulk_create(likes)
                counter += 1
            except IntegrityError:
                pass

    def create_tags(self, tags_quantity, chunks_quantity=10):
            
        chunk_size = int(tags_quantity / chunks_quantity)

        questions_last = Question.objects.last().id
        
        for i in range(chunks_quantity):

            tags = [Tag(name=self.fake.unique.catch_phrase())
                    for j in range(chunk_size)]
            tags = Tag.objects.bulk_create(tags)

            for tag in tags:
                tag.questions.add(*[randint(1, questions_last) for j in range(20)])

    def handle(self, *args, **options):
        profiles_quantity = options["ratio"]
        questions_quantity = options["ratio"] * 10
        answers_quantity = options["ratio"] * 100
        tags_quantity = options["ratio"]
        likes_quantity = options["ratio"] * 200

        self.create_profiles(profiles_quantity)
        print("CREATED PROFILES\n")

        self.create_questions(questions_quantity)
        print("CREATED QUESTIONS\n")

        self.create_answers(answers_quantity, profiles_quantity)
        print("CREATED ANSWERS\n")

        self.create_likes(likes_quantity)
        print("CREATED LIKES\n")

        self.create_tags(tags_quantity)
        print("CREATED TAGS\n")
