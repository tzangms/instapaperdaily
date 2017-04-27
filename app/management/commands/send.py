from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings

from templated_email import send_templated_mail

from app.instapaper import Instapaper

class Command(BaseCommand):

    def handle(self, *args, **options):
        for user in User.objects.all():
            instapaper = Instapaper(
                settings.INSTAPAPER_KEY, settings.INSTAPAPER_SECRET, 
                user.profile.oauth_token, user.profile.oauth_token_secret)

            bookmarks = instapaper.get_bookmarks(limit=3)

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
