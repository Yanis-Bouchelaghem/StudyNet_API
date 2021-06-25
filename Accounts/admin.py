from django.contrib import admin

from .models import User,Teacher,Student
from .forms import CustomUserAdmin

admin.site.site_header = 'Studynet administration'

class EnseignantAdmin(admin.ModelAdmin):
    list_display = ('user','grade','department')
    #Enable search fields using teacher's email, his grade and his department's name and code
    search_fields = ('user__email','grade','department__name','department__code')
    #Enable filtering by grade and department
    list_filter = ('grade','department')
# Register your models here.

admin.site.register(User,CustomUserAdmin)
admin.site.register(Teacher, EnseignantAdmin)
admin.site.register(Student)
