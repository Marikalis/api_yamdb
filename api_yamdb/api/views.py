from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
# from django.core.exceptions import ValidationError
from rest_framework import status


from .permissions import IsAdmin
from reviews.models import User
from .serializers import SignupSerializer, ConfirmationSerializer, UserSerializer
from .tokens import account_activation_token


EMAIL_SUBJECT = 'Код регистрации аккаунта'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin,)
    lookup_field = 'username'
    pagination_class = LimitOffsetPagination

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def users_profile(self, request):
        user = get_object_or_404(
            User,
            username=request.user.username)

        if request.method == 'PATCH':
            serializer = UserSerializer(
                user,
                context={'request': request},
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(user)

        return Response(serializer.data)


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
    permission_classes = (permissions.AllowAny,)

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
