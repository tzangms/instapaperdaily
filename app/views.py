from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import auth

from .models import Profile

from .forms import SigninForm
from .instapaper import Instapaper


def home(request):
    return render(request, 'index.html')


def signin(request):

    form = SigninForm(request.POST or None)
    if form.is_valid():
        oauth_token = form.cleaned_data['oauth_token']
        oauth_token_secret = form.cleaned_data['oauth_token_secret']

        instapaper = Instapaper(
            settings.INSTAPAPER_KEY, settings.INSTAPAPER_SECRET, oauth_token, oauth_token_secret)

        insta_user = instapaper.verify_credentials()

        try:
            profile = Profile.objects.get(uid=insta_user['user_id'])
        except Profile.DoesNotExist:
            
            #
            password = User.objects.make_random_password()
            username = insta_user['username']

            try:
                user = User.objects.get(username=username)
                profile = user.profile
            except User.DoesNotExist:
                user = User.objects.create_user(username=username, email=username, password=password)

                profile = Profile()
                profile.user = user
                profile.uid = insta_user['user_id']
                profile.oauth_token = oauth_token
                profile.oauth_token_secret = oauth_token_secret
                profile.save()

        user = auth.authenticate(uid=profile.uid)
        if user:
            auth.login(request, user)
            return redirect('/success/')
        
    return render(request, 'signin.html', {'form': form})

def success(request):
    return render(request, 'success.html')
