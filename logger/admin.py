from django.contrib import admin
from .models import LogEntry


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'level', 'message', 'data')
    # This will add a filter sidebar in the admin for 'level'
    list_filter = ('level',)


admin.site.register(LogEntry, LogEntryAdmin)
