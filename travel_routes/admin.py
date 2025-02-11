from django.contrib import admin
from .models import BannedWord

@admin.register(BannedWord)
class BannedWordAdmin(admin.ModelAdmin):
    list_display = ('word',)
    search_fields = ('word',)
