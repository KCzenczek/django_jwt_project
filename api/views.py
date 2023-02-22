from django.contrib.auth.models import User
from api.serializers import UserSerializer
from rest_framework import generics

#TODO finish endpoint auth
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
