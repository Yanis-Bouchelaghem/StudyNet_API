from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django import forms

from .models import User,Teacher,Student
#Inlines
class StudentInline(admin.TabularInline):
    model = Student
    verbose_name = _('Student')
    verbose_name_plural = _('Student') #There is only going to be one student reference.
    extra = 1
    can_delete = False

class TeacherInline(admin.TabularInline):
    model = Teacher
    verbose_name = _('Teacher')
    verbose_name_plural = _('Teacher') #There is only going to be one teacher reference.
    extra = 1
    show_change_link=True
    can_delete = False


class CustomUserAdmin(UserAdmin):
    # Admin interface logic for user creation and modification
    model = User
    fieldsets = (
        (None, {'fields': ('id','email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Type'), {'fields': ('user_type',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_complete', 'is_staff', 'is_superuser','groups')}),
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
    readonly_fields = ('id','last_login','date_joined','is_complete',)
    ordering = ('-date_joined',)
    list_filter = ('user_type','is_active')
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
            #If a superuser is being created, check that the creator is a superuser or an admin
            if obj.user_type == User.Types.SUPERUSER and request.user.user_type != User.Types.SUPERUSER:
                raise forms.ValidationError({'user_type':'Only superusers can create other superusers.'})
            #If an admin is being created, give him staff permission and add him to the administrator group
            if obj.user_type == User.Types.ADMINISTRATOR:
                obj.is_staff = True
                obj.save()
                admin_group = Group.objects.get(name='Administrator')
                admin_group.user_set.add(obj)
                

        else:
            if not obj.is_complete:
                #If a student's information is completed, mark him as complete and activate him.
                if obj.user_type == User.Types.STUDENT and hasattr(obj,'student'):
                    obj.is_complete = True
                    obj.is_active = True
                #If a teacher's information is completed, mark him as complete and activate him.
                elif obj.user_type == User.Types.TEACHER and hasattr(obj,'teacher'):
                    obj.is_complete = True
                    obj.is_active = True
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        temp_readonly_fields = self.readonly_fields
        if obj:
            #Cannot edit the user type after the user has been created.
            temp_readonly_fields += ('user_type',)
            #If the account is not complete, don't let the admin user activate it.
            if not obj.is_complete:
                temp_readonly_fields += ('is_active',)
        return temp_readonly_fields