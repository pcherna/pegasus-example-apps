from django import forms

from .models import Puma

class PumaForm(forms.ModelForm):
    class Meta:
        model = Puma
        fields = [
            'name', 'number', 'notes',
        ]
