from django.contrib import admin
from .models import Toad

@admin.register(Toad)
class ToadAdmin(admin.ModelAdmin):
    # Fields to include in admin's list view
    list_display = ['name', 'number']
