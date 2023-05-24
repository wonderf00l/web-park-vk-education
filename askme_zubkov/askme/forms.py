from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from .models import *
from django.conf import settings
from os import remove
from django.core.exceptions import ObjectDoesNotExist



class AddQuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['title', 'content']
        # widgets = {
        #     'title': forms.TextInput(),
        #     'content': forms.Textarea(attrs={'cols': 60, 'rows': 10})
        # }

    # def __init__(self, user=None, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.user = user

    tags = forms.CharField(max_length=255, required=True)

    def clean_tags(self, *args, **kwargs): # after general clean

        tags_str = self.cleaned_data['tags']
        tags = tags_str.split(',')

        if len(tags) > 3:
            raise ValidationError('More than 3 tags', code=1)
        if tags_str.count(',') != len(tags) - 1:
            raise ValidationError('Wrong input for tags', code=2)

        return tags

    def save(self,user_,commit=True):
        question = super().save(commit=False) # write part of form data to the db but witouh adding to the db
        question.author = user_
        question.save()

        for tag_name in self.cleaned_data['tags']:
            try:
                Tag.objects.get(name=tag_name).questions.add(question)
            except ObjectDoesNotExist:
                new_tag = Tag.objects.create(name=tag_name)
                new_tag.questions.add(question)

        return question



class UserRegisterForm(UserCreationForm): # поля паролей и валидация у родителя

    avatar = forms.ImageField(required=False) # initial=settings.MEDIA_ROOT + '/' + Profile.avatar.field.default)

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'email', 'first_name', 'last_name')

    def save(self, commit=True):
        user_ = super().save(commit)
        avatar_ = self.cleaned_data.get('avatar')
        Profile.objects.create(avatar=(avatar_ if avatar_ else Profile.avatar.field.default), user=user_) # settings.MEDIA_ROOT + Profile.avatar.field.default
        return user_        # settings.MEDIA_URL + Profile.avatar.field.default - префикс не нужен, т.к. он подставляется благодаря парметру upload_to



class UserSettingsForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        fields = ('username', 'email', 'first_name', 'last_name')

    password = None
    avatar = forms.ImageField(required=False)

    def save(self, commit=True):
        super().save(commit=False)
        avatar_ = self.cleaned_data.pop('avatar')
        user = User.objects.filter(username=self.cleaned_data['username'])
        if user.update(**self.cleaned_data):
            profile = user[0].profile
            if avatar_:
                if profile.avatar.url != settings.MEDIA_URL + profile.avatar.field.default:
                    remove(profile.avatar.path)
                profile.avatar = avatar_
                profile.save()
        else:
            raise ValidationError
        return user
