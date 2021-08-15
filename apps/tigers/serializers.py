from rest_framework import serializers

from .models import Tiger


class TigerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tiger
        fields = ('id', 'name', 'number', 'notes')
