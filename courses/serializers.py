from rest_framework import serializers

from .models import Section


class SectionSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()

    class Meta:
        model = Section
        fields = ['course', 'number', 'title']
