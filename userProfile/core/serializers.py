from rest_framework import serializers
from django.contrib.auth.models import User
from .models import userProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email','password']

class ProfileSerialier(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = userProfile
        fields = '__all__'

