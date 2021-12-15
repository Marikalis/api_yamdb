from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework import status


from reviews.models import User
from .serializers import UserSerializer
from .tokens import account_activation_token


EMAIL_SUBJECT = 'Код регистрации аккаунта'


class CreateUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get_or_create(
                User,
                username=serializer.data.get('username'))
            msg = account_activation_token.make_token(user)
            send_mail(
                'Ваш код тута',
                msg,
                'server@server.serve',
                [user.email],
                fail_silently=True
            )
            return Response(
                'Проверьте вашу почту туда прилетело письмецо',
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'username': ['Где?'],
                    'email': ['Тоже надо бы']
                },
                status=status.HTTP_400_BAD_REQUEST
            )
