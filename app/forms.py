from django import forms
from django.conf import settings

from .instapaper import Instapaper, LoginError


class SigninForm(forms.Form):
    username = forms.CharField(label='Email', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        instapaper = Instapaper(
            settings.INSTAPAPER_KEY, settings.INSTAPAPER_SECRET)
        try:
            token = instapaper.login(username, password)
        except LoginError:
            raise forms.ValidationError('Please make sure your email and password is correct.')

        self.cleaned_data['oauth_token'] = token.key
        self.cleaned_data['oauth_token_secret'] = token.secret
