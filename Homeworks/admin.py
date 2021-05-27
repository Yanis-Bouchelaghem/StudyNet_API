from django.contrib import admin
from .models import Homework,HomeworkHistory

class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('title','assignment','due_date','due_time')
    #Enable searching using title, teacher's email, sections, and module's name and code.
    search_fields = ('title',
    'assignment__teacher_section__teacher__user__email',
    'assignment__teacher_section__section__code',
    'assignment__module_section__module__name',
    'assignment__module_section__module__code')
    #Enable filtering by due date and sections.
    list_filter = ('due_date','assignment__module_type','assignment__teacher_section__section')

class HomeworkHistoryAdmin(admin.ModelAdmin):
    list_display = ('teacher','section','module',
    'module_type','concerned_groups','due_date','due_time','action_date','action_type','author')
    search_fields = ('teacher__user__email','author__email','section__code','module__code','module__name','module_type')
    list_filter = ('action_date','action_type','due_date','module_type')

# Register your models here.
admin.site.register(Homework,HomeworkAdmin)
admin.site.register(HomeworkHistory,HomeworkHistoryAdmin)