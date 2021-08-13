from django import forms

from .models import Frog

class FrogForm(forms.ModelForm):
    class Meta:
        model = Frog
        
        fields = [
            'name', 'number', 'notes',
        ]
