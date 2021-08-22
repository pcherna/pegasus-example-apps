from django import forms

from .models import Polliwog

class PolliwogForm(forms.ModelForm):
    class Meta:
        model = Polliwog
        
        fields = [
            'name', 'number', 'notes',
        ]
