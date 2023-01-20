from django.contrib.auth.models import User
from api.serializers import UserSerializer
from rest_framework import generics


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
