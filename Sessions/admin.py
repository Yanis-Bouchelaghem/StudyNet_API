from django.contrib import admin
from .models import Session,SessionHistory
# Register your models here.
admin.site.register(Session)
admin.site.register(SessionHistory)