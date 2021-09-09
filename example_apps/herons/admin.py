from django.contrib import admin
from .models import Heron

@admin.register(Heron)
class HeronAdmin(admin.ModelAdmin):
    # Fields to include in admin's list view
    list_display = ['name', 'number']
