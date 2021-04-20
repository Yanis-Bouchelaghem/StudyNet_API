from django.contrib import admin
from .models import Department,Specialty,Section,Module,TeacherSection,Assignment

# Register your models here.

admin.site.register(Department)
admin.site.register(Specialty)
admin.site.register(Section)
admin.site.register(Module)
admin.site.register(TeacherSection)
admin.site.register(Assignment)
