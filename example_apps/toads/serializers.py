from rest_framework import serializers

from .models import Toad


class ToadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Toad
        fields = ('id', 'name', 'number', 'notes')
