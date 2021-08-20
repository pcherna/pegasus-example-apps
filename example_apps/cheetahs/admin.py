from django.contrib import admin
from .models import Cheetah

@admin.register(Cheetah)
class CheetahAdmin(admin.ModelAdmin):
    # Fields to include in admin's list view
    list_display = ['name', 'number']
