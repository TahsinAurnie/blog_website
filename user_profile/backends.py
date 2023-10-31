from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ObjectDoesNotExist
from .models import User

class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username: None, password: None, **kwargs):
        try:
            user = User.objects.get(email = username)    # checking with field element get from form whether it has got email
            if user.check_password(password):
                return user
            else: 
                return None
        except ObjectDoesNotExist:
            return None

    def get_user(self, user_id: int):
        try:
            user = User.objects.get(pk = user_id)
            return user
        except ObjectDoesNotExist:
            return None


