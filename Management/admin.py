from django.contrib import admin
from .models import Department,Specialty,Section,Module,TeacherSection,Assignment,ModuleSection


#inlines
class ModulesInline(admin.TabularInline):
    model = ModuleSection
    verbose_name = 'Module'
    verbose_name_plural = 'Modules'
    extra = 0

class SectionAdmin(admin.ModelAdmin):
    inlines = [ModulesInline,]
# Register your models here.
admin.site.register(Department)
admin.site.register(Specialty)
admin.site.register(Section,SectionAdmin)
admin.site.register(Module)
admin.site.register(TeacherSection)
admin.site.register(Assignment)
