from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('domain', 'can_edit')

class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'is_superuser', 'roles')
