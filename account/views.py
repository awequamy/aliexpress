from urllib import response
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from . import serializers
from .send_email import send_confirmation_email,send_reset_password
from django.contrib.auth import get_user_model
from aliexpress.tasks import send_email_task
# from account.send_email import send_html_email

User=get_user_model()


class RegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                send_confirmation_email(user,)
            return Response(serializer.data, status=201)
        return Response(status=400)

class ActivationView(APIView):
    permission_classes=(permissions.AllowAny,)
    def get(self,request,activation_code):
        try:
            user=User.objects.get(activation_code=activation_code)
            user.is_active=True
            user.activation_code=''
            user.save()
            return Response({
                'msg': 'You successfully activated your account!'},
                status=200
            )
        except User.DoesNotExist:
            return Response(
                {'msg':'Link has already expired, try another one'},
                status=400
            )

class LoginApiView(TokenObtainPairView):
    serializer_class=serializers.LoginSerializer


class LogoutApiView(GenericAPIView):
    serializer_class=serializers.LogoutSerializer
    permission_classes=(permissions.IsAuthenticated,)
    def post(self,request,*args):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Successfully logged out!',status=204)

class ForgotPasswordView(APIView):
    permission_classes=(permissions.AllowAny,)
    def post(self,request):
        serializer=serializers.ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user=User.objects.get(email=serializer.data.get('email'))
            user.create_activation_code()
            user.save()
            send_reset_password(user)
            return Response('Check your mail!',status=200)

        except User.DoesNotExist:
            return Response('User with this email does not exist!',status=400)

class RestorePasswordView(APIView):
    permission_classes=(permissions.AllowAny,)
    def post(self,request):
        serializer=serializers.RestorePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Password was successfully changed!',status=200)

class FollowSpamApi(APIView):
    permission_classes=(permissions.AllowAny,)
    def post(self, request):
        serializer=serializers.SpamViewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # send_html_email()
        return Response('esheeeek!!!!!!',status=200)

