from django.db import models
import json


class LogEntry(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=10, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    data = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.level} - {self.message}"
