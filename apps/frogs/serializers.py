from rest_framework import serializers

from .models import Frog


class FrogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Frog
        fields = ('id', 'name', 'number', 'notes')
