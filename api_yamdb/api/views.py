from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
# from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework_jwt.settings import api_settings


from .permissions import IsAdmin
from reviews.models import User
from .serializers import SignupSerializer, ConfirmationSerializer, UsersSerializer
from .tokens import account_activation_token


EMAIL_SUBJECT = 'Код регистрации аккаунта'


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = LimitOffsetPagination


class UsernameViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = LimitOffsetPagination

    def get_user(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return user

    def get_queryset(self):
        return self.get_user()


class CreateUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user, created = User.objects.get_or_create(
                username=serializer.data.get('username'),
                email=serializer.data.get('email')
            )
            user.is_active = False
            user.save()
            msg = account_activation_token.make_token(user)
            email = EmailMessage(
                EMAIL_SUBJECT,
                msg,
                to=[serializer.data.get('email')]
            )
            email.send()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class ValidationUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)

    def create(self, request):
        serializer = ConfirmationSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User,
                username=serializer.data.get('username'))
            confirmation_code = serializer.data.get('confirmation_code')
            if user is not None and user.is_active is not True and account_activation_token.check_token(user, confirmation_code):
                user.is_active = True
                user.save()
                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

                payload = jwt_payload_handler(request.user)
                token = jwt_encode_handler(payload)
                return Response(
                    {
                        'token': token
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    'Неверный код активации',
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
