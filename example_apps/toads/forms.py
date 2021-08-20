from django import forms

from .models import Toad

class ToadForm(forms.ModelForm):
    class Meta:
        model = Toad
        
        fields = [
            'name', 'number', 'notes',
        ]
