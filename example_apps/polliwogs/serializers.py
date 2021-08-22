from rest_framework import serializers

from .models import Polliwog


class PolliwogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Polliwog
        fields = ('id', 'name', 'number', 'notes')
