from django.contrib import admin
from .models import Puma

@admin.register(Puma)
class PumaAdmin(admin.ModelAdmin):
    # Fields to include in admin's list view
    list_display = ['name', 'number']
