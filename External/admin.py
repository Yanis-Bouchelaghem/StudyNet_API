from django.contrib import admin
from .models import AppVersionSupport

class AppVersionAdmin(admin.ModelAdmin):
    list_display = ('version','is_supported')
    search_fields = ('version',)
    list_filter = ('is_supported',)
# Register your models here.
admin.site.register(AppVersionSupport,AppVersionAdmin)