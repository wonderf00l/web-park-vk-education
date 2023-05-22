from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from .models import *


class AddQuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10})
        }
    # redefine default model titles
class AddTagForm(forms.Form): # при использовании ModelForm ошибка при tag_form.save(), т.к. не удается проинициализировать поле author_id

    tag = forms.CharField(required=True, max_length=255, empty_value='some_tag', widget=forms.TextInput())

    # def clean():
    #     cleaned_data = super().clean()
    #     tag_name = cleaned_data.get('tag')

    # class Meta:
    #     model = Tag
    #     fields = ['name'] # redefine name to 'Tag'
        # maybe link my custom styles

class UserRegisterForm(UserCreationForm): # Profile creation in UserChangeForm (user settings)
    class Meta(UserCreationForm.Meta):
        fields = ('username', 'email', 'first_name', 'last_name')

    avatar = forms.ImageField(required=False, allow_empty_file=True)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.id = User.objects.last().id + 1
        user.save()
        return user











# !label=our_name, required, initial
# widget = forms.TextInput(attrs={'class':'form-input'})



#     def save(self, commit=True):
#         user = super().save(commit=False)
#         profile_form = ProfileRegisterForm({'avatar': self.cleaned_data['avatar'], 'user': user}) # возмонжо, нужно убрать проверку user вообще и сдлеать profiel форму обычной
#         if commit:
#             try:
#                 profile_form.save() # как проверит user?
#             except:
#                 msg = "Smth went wrong with ProfileRegistration"
#                 self.add_error('avatar', msg)
#         return user
        
# class ProfileRegisterForm(forms.ModelForm):

#     class Meta:
#         model = Profile
#         fields = ['user']
    
