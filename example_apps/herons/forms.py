from django import forms

from .models import Heron

class HeronForm(forms.ModelForm):
    class Meta:
        model = Heron
        fields = [
            'name', 'number', 'notes',
        ]
