from django.contrib import admin
from .models import Polliwog

@admin.register(Polliwog)
class PolliwogAdmin(admin.ModelAdmin):
    # Fields to include in admin's list view
    list_display = ['name', 'number']
