from rest_framework.serializers import ModelSerializer
from .models import *


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name', 'description', 'year']


from django.contrib.auth.models import User
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password']
