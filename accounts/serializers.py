from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from rest_framework import serializers as drf_serializers
from rest_framework.settings import api_settings
from django.contrib.auth.hashers import make_password

User = get_user_model()

#For creating user accounts
from rest_framework import serializers
from .models import UserAccount

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = [
            'email', 
            'full_name', 
            'password',
            'uid', 
            'card', 
            'access_lvl',
            'sex', 
            'job_title', 
            'email2', 
            'birthday', 
            'hiredday', 
            'street', 
            'city', 
            'state', 
            'zip', 
            'ophone', 
            'deptid', 
            'photos',
            'status'
        ] 


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not instance.photos or not instance.photos.name:
            representation['photos'] = None
        else:
            representation['photos'] = instance.photos.url  
        return representation

    def update(self, instance, validated_data):
        # Update fields from validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Handle password update
        
        instance.save()
        return instance

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")

        if password is not None:
            try:
                validate_password(password, user)
            except django_exceptions.ValidationError as e:
                serializer_error = drf_serializers.as_serializer_error(e)
                raise drf_serializers.ValidationError(
                    {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
                )

        return attrs
