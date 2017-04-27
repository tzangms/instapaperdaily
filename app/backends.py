from django.contrib.auth.models import User
from app.models import Profile

class InstapaperBackend:
    """
    InstapaperBackend for authentication  
    """

    supports_anonymous_user = False
    supports_object_permissions = False
    supports_inactive_user = False

    def authenticate(self, uid, user=None):
        '''
        authenticates the token by requesting user information from twitter
        '''

        try:
            profile = Profile.objects.get(uid=uid)
            return profile.user
        except Profile.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except:
            return None
