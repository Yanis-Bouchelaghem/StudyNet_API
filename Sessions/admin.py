from django.contrib import admin
from .models import Session,SessionHistory

#Model admins
class SessionAdmin(admin.ModelAdmin):
    list_display = ('assignment','concerned_groups','day',
    'start_time','end_time')
    search_fields = ('day',
    'assignment__teacher_section__teacher__user__email',
    'assignment__teacher_section__section__code',
    'assignment__module_section__module__name',
    'assignment__module_section__module__code')
    list_filter = ('day','assignment__module_type','assignment__teacher_section__section')

class SessionHistoryAdmin(admin.ModelAdmin):
    list_display = ('teacher','section','module',
    'module_type','concerned_groups','start_time','end_time','action_date','action_type','author')
    search_fields = ('teacher__user__email','author__email','section__code','module__code','module__name','module_type')
    list_filter = ('action_date','action_type','module_type')
# Register your models here.
admin.site.register(Session,SessionAdmin)
admin.site.register(SessionHistory,SessionHistoryAdmin)