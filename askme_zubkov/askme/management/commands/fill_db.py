from django.core.management.base import BaseCommand
from askme.models import User, Profile, Question, Answer, Tag, Assessment
from faker import Faker
from django.contrib.contenttypes.models import ContentType
from random import randint

# obj_id = randint - without QuierySets
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

    def create_profiles(self, profiles_quantity):

        User.objects.bulk_create([  # DuplicateError with user = self.fake.unique.simple_profile()["username"]
            User(username=self.fake.unique.company(),
                 email=self.fake.unique.company() + self.email_samples[randint(0, len(self.email_samples) - 1)], password=self.fake.name(), last_login=self.fake.date_time())
            for i in range(profiles_quantity)
        ])

        Profile.objects.bulk_create([
            Profile(avatar=self.img_url_prefix + str(i + 1), user_id=i + 1)
            for i in range(profiles_quantity)
        ])

    def create_questions(self, questions_quantity):

        profiles = User.objects.all()

        Question.objects.bulk_create([
            Question(title=self.fake.unique.catch_phrase(
            ), content=self.fake.text(), author=profiles[randint(0, len(profiles) - 1)])
            for i in range(questions_quantity)
        ])

    def create_answers(self, answers_quantity, profiles_quantity):

        profiles = User.objects.all()
        questions = Question.objects.all()

        Answer.objects.bulk_create([
            Answer(content=self.fake.text(), correctness_degree=randint(1, profiles_quantity), author=profiles[randint(0, len(profiles) - 1)],
                   question=questions[randint(0, len(questions) - 1)])
            for i in range(answers_quantity)
        ])

    def create_assessments(self, assessments_quantity):

        types = [
            "like",
            "dislike"
        ]

        ct_question, ct_answer = ContentType.objects.get_for_model(
            Question), ContentType.objects.get_for_model(Answer)
        content_types = (ct_question, ct_answer)

        profiles = User.objects.all()
        questions = Question.objects.all()
        answers = Answer.objects.all()

        assessments = list()

        for i in range(assessments_quantity):
            content_type_ = content_types[randint(0, len(content_types) - 1)]
            obj_id = randint(1, len(questions)) if content_type_ == ct_question else randint(
                1, len(answers))
            assessments.append(Assessment(type=types[randint(0, len(
                types) - 1)], content_type=content_type_, object_id=obj_id, author=profiles[randint(0, len(profiles) - 1)]))

        # check that 1 author -- 1 like/dislike or 1 like/dis + 1 dislike/like (Model.objects.annotate(group by author id) --> check len(value) --> if != 1 and like/dislike only --> exception)

        Assessment.objects.bulk_create(assessments)

    def create_tags(self, tags_quantity):
        questions = Question.objects.all()

        tags = [Tag(name=self.fake.unique.catch_phrase())
                for i in range(tags_quantity)]
        Tag.objects.bulk_create(tags)

        for tag in tags:
            tag.question.add(questions[randint(0, len(questions) - 1)])

    def handle(self, *args, **options):
        profiles_quantity = options["ratio"]
        questions_quantity = options["ratio"] * 10
        answers_quantity = options["ratio"] * 100
        tags_quantity = options["ratio"]
        assessments_quantity = options["ratio"] * 200

        self.create_profiles(profiles_quantity)
        print("CREATED PROFILES\n")

        self.create_questions(questions_quantity)
        print("CREATED QUESTIONS\n")

        self.create_answers(answers_quantity, profiles_quantity)
        print("CREATED ANSWERS\n")

        self.create_assessments(assessments_quantity)
        print("CREATED ASSESSMENTS\n")

        self.create_tags(tags_quantity)
        print("CREATED TAGS\n")
