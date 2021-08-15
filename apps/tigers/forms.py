from django import forms

from .models import Tiger

class TigerForm(forms.ModelForm):
    class Meta:
        model = Tiger
        fields = [
            'name', 'number', 'notes',
        ]
