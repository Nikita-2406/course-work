from rest_framework import serializers
from app.models import Users, Files, Session

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'name', 'login', 'password', 'admin']

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = ['id', 'file_name', 'file_link', 'date', 'user_id']

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['login', 'password']