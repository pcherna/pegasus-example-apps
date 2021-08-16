from rest_framework import serializers

from .models import Cheetah


class CheetahSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cheetah
        fields = ('id', 'name', 'number', 'notes')
