"""A class for jwt authentication."""

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
import jwt

SECRET_KEY = "secret"

class JWTBackend(ModelBackend):
    def authenticate(self, request, jwt_token=None, **kwargs):
        if not jwt_token:
            return None

        try:
            email = jwt.decode(jwt_token, SECRET_KEY , algorithms=["HS256"]).get("email")
            if not email:
                return None
            else:
                UserModel = get_user_model()
                try:
                    user = UserModel.objects.get(email=email)
                    return user
                except UserModel.DoesNotExist:
                    return None
        except Exception:
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None