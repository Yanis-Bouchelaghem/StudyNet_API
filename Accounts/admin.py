from django.utils.translation import ugettext_lazy as _

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Teacher,Student

#Inlines
class StudentInline(admin.TabularInline):
    model = Student
    verbose_name = _('Student')
    verbose_name_plural = _('Student') #There is only going to be one student reference.
    extra = 1
    show_change_link=True
    can_delete = False

class TeacherInline(admin.TabularInline):
    model = Teacher
    verbose_name = _('Teacher')
    verbose_name_plural = _('Teacher') #There is only going to be one teacher reference.
    extra = 1
    show_change_link=True
    can_delete = False

class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances.
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    model = User
    fieldsets = (
        (None, {'fields': ('id','email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Type'), {'fields': ('user_type',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_complete', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','first_name','last_name','password1','password2','user_type')}
        ),
    )
    
    list_display = ('email', 'first_name', 'last_name','user_type')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('id','last_login','date_joined')
    ordering = ('email',)
    inlines = []

    def get_inlines(self,request, obj):
        #Insert the information relevant to this type of user.
        if obj :
            if obj.user_type == User.Types.STUDENT:
                return [StudentInline,]
            elif obj.user_type == User.Types.TEACHER:
                return [TeacherInline,]
        return self.inlines

    def save_model(self, request, obj, form, change):
        if not change:
            #If a student or a teacher is being created, mark him as incomplete and keep him deactivated.
            if obj.user_type == User.Types.STUDENT or obj.user_type == User.Types.TEACHER:
                obj.is_complete = False
                obj.is_active = False
        else:
            if not obj.is_complete:
                #If a student has his information completed, mark him as complete and activate him.
                if obj.user_type == User.Types.STUDENT and hasattr(obj,'student'):
                    obj.is_complete = True
                    obj.is_active = True
                #If a teacher has his information completed, mark him as complete and activate him.
                elif obj.user_type == User.Types.TEACHER and hasattr(obj,'teacher'):
                    obj.is_complete = True
                    obj.is_active = True
        super().save_model(request, obj, form, change)

# Register your models here.

admin.site.register(User,CustomUserAdmin)
admin.site.register(Teacher)
admin.site.register(Student)
