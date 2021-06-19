from django.db import models
from django.db.models import fields
from rest_framework import serializers
from students.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email']