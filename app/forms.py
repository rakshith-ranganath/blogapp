from django import forms
from app.models import Comments, Subscribe, Profile
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = {'content', 'email', 'name', 'website'}


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['placeholder'] = 'Type your comment......'
        self.fields['email'].widget.attrs['placeholder'] = 'email'
        self.fields['name'].widget.attrs['placeholder'] = 'name'
        self.fields['website'].widget.attrs['placeholder'] = 'wesite'

class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = '__all__'
        labels = {'email':_('')}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email.'


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {'username', 'first_name', 'last_name', 'email'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'