from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.core.mail import send_mail
from django.http import HttpResponse
# from django.core.exceptions import ValidationError
from rest_framework import status


from reviews.models import User
from .serializers import UserSerializer, ConfirmationSerializer
from .tokens import account_activation_token


EMAIL_SUBJECT = 'Код регистрации аккаунта'


class CreateUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user, created = User.objects.get_or_create(
                username=serializer.data.get('username')
            )
            user.is_active = False
            user.save()
            msg = account_activation_token.make_token(user)
            send_mail(
                EMAIL_SUBJECT,
                msg,
                'server@server.serve',
                [serializer.data.get('email')],
                fail_silently=True
            )
            return Response(
                f'Проверьте вашу почту {msg}',
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class ValidationUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = ConfirmationSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(username=serializer.data.get('username'))
            confirmation_code = serializer.data.get('confirmation_code')
            if user is not None and user.is_active is not True and account_activation_token.check_token(user, confirmation_code):
                user.is_active = True
                user.save()
                return Response(
                    {
                        'token': 'todo'
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
