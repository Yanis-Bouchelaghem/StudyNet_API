from django.utils.translation import ugettext_lazy as _

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Teacher,Student

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

# Register your models here.

admin.site.register(User,CustomUserAdmin)
admin.site.register(Teacher)
admin.site.register(Student)
