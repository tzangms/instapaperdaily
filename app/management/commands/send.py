import random

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings

from templated_email import send_templated_mail

from app.instapaper import Instapaper

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--email', nargs='+')

    def handle(self, *args, **options):
        users = User.objects.all()

        if options['email']:
            users = users.filter(email__in=options['email'])

        for user in users:
            print("Processing for {}".format(user.email))
            instapaper = Instapaper(
                settings.INSTAPAPER_KEY, settings.INSTAPAPER_SECRET, 
                user.profile.oauth_token, user.profile.oauth_token_secret)


            # random
            bookmarks = instapaper.get_bookmarks(limit=200)
            bookmarks = random.sample(bookmarks, 3)

            
            # bypass who has no bookmarks
            if len(bookmarks) == 0:
                continue

            # get subject
            subject = bookmarks[0].title

            # render email template
            send_templated_mail(
                template_name='daily',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                context={
                    'subject': subject,
                    'bookmarks': bookmarks,
                },
            )

            # archive bookmarks
            for bookmark in bookmarks:
                bookmark.archive()
