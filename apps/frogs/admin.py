from django.contrib import admin
from .models import Frog

@admin.register(Frog)
class FrogAdmin(admin.ModelAdmin):
    # Fields to include in admin's list view
    list_display = ['name', 'number']
