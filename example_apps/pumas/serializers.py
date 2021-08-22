from rest_framework import serializers

from .models import Puma


class PumaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Puma
        fields = ('id', 'name', 'number', 'notes')
