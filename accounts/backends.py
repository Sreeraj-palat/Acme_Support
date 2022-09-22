from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Account


Account = get_user_model()


class EmailPhoneUsernameAuthenticationBackend(object):
    def authenticate(self, request, username=None, password=None):
        try:
            user = Account.objects.get(
                Q(username=username) | Q(phone_number=username) | Q(email=username)
            )

        except Account.DoesNotExist:
            return None

        if user and check_password(password, user.password):
            return user

        return None

    def get_user(self, user_id):
        try:
            return Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            return None