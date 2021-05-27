from django.contrib import admin
from .models import Department,Specialty,Section,Module,TeacherSection,Assignment,ModuleSection


#inlines
class ModulesInline(admin.TabularInline):
    model = ModuleSection
    verbose_name = 'Module'
    verbose_name_plural = 'Modules'
    extra = 0
#Admin models
class SectionAdmin(admin.ModelAdmin):
    list_display = ('code','number_of_groups','specialty')
    search_fields = ('code','number_of_groups','specialty__name','specialty__code')
    list_filter = ('specialty__department',)
    inlines = [ModulesInline,]

class ModuleAdmin(admin.ModelAdmin):
    list_display = ('code','name','types')
    search_fields = ('code','name','types')

class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('code','name','department')
    search_fields = ('code','name','department__name','department__code')
    list_filter = ('department',)

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code','name')
    search_fields = ('code','name')

class TeacherSectionAdmin(admin.ModelAdmin):
    list_display = ('teacher','section')
    search_fields = ('teacher__user__email','section__code')
    list_filter = ('section__specialty__department',)

# Register your models here.
admin.site.register(Department,DepartmentAdmin)
admin.site.register(Specialty,SpecialtyAdmin)
admin.site.register(Section,SectionAdmin)
admin.site.register(Module,ModuleAdmin)
admin.site.register(TeacherSection,TeacherSectionAdmin)
admin.site.register(Assignment)
