from django.contrib import admin

from .models import User,Teacher,Student
from .forms import CustomUserAdmin


# Register your models here.

admin.site.register(User,CustomUserAdmin)
admin.site.register(Teacher)
admin.site.register(Student)
