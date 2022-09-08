from abc import ABC

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import models
from django.db.models import fields
from knox.serializers import UserSerializer as knoxUserSerializer
from rest_framework import serializers

from time_tracker.serializers import ProjectSerializer


class UserSerializer(serializers.ModelSerializer):
    member_in_projects = ProjectSerializer(many=True, read_only=True)
    owner_of_projects = ProjectSerializer(many=True, read_only=True)#931155

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'member_in_projects', 'owner_of_projects']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Incorrect Credentials Passed.')
