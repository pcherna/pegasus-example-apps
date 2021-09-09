from rest_framework import serializers

from .models import Heron


class HeronSerializer(serializers.ModelSerializer):

    class Meta:
        model = Heron
        fields = ('id', 'name', 'number', 'notes')
