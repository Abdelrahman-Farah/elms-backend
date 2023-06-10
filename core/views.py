from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
class CustomUserLoginView(APIView):
    User = get_user_model()
    def post (self, request):
        username = request.data['username']
        password = request.data['password']

        queryset = self.User.objects.filter(username = username)

        if not queryset:
            return Response('No account found with the given credentials.', status=status.HTTP_401_UNAUTHORIZED)

        user = queryset[0]

        if check_password(password, user.password) == False:
            return Response('Wrong password was provided.', status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            email = user.email

            protocol = 'https://' if request.is_secure() else 'http://'
            web_url = protocol + request.get_host()
            post_url = web_url + "/auth/users/resend_activation/"
            post_data = {'email': email}
            result = requests.post(post_url, data = post_data)
            # content = result.text

            return Response('Your account is not active, Activation mail sent.', status=status.HTTP_403_FORBIDDEN)

        tokens = TokenObtainPairSerializer.get_token(user)
        parse_token = {
            'refresh': str(tokens),
            'access': str(tokens.access_token),
        }
        return Response(data=parse_token, status=status.HTTP_200_OK)


class CustomResetPasswordView(APIView):
    User = get_user_model()
    def post (self, request):
        email = request.data['email']

        try:
            validate_email(email)
        except ValidationError as e:
            return Response({'email':['Enter a valid email address.']}, status=status.HTTP_401_UNAUTHORIZED)

        queryset = self.User.objects.filter(email = email)

        if not queryset:
            return Response(status=status.HTTP_204_NO_CONTENT)

        user = queryset[0]
        active = user.is_active

        if not active:
            user.is_active = True
            user.save()

        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol + request.get_host()
        post_url = web_url + "/auth/users/reset_password/"
        post_data = {'email': email}
        requests.post(post_url, data = post_data)

        if not active:
            user.is_active = False
            user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
