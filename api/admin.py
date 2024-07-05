from django.contrib import admin

from .models import (
    Task,
    Log
)

# Register your models here.

admin.site.register(Task)
admin.site.register(Log)
