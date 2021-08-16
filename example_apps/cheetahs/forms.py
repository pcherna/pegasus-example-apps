from django import forms

from .models import Cheetah

class CheetahForm(forms.ModelForm):
    class Meta:
        model = Cheetah
        fields = [
            'name', 'number', 'notes',
        ]
