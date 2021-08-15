from django.contrib import admin
from .models import Tiger

@admin.register(Tiger)
class TigerAdmin(admin.ModelAdmin):
    # Fields to include in admin's list view
    list_display = ['name', 'number']
