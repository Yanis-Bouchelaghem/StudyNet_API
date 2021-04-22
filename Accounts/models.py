from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.utils.http import urlquote
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _

class UserManager(BaseUserManager):
    """
    The manager that will handle the creation of users.
    """
    def _create_user(self, email,first_name,last_name, password,is_staff, is_superuser,
     user_type,is_active,is_complete):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The user must have an Email.')
        if not first_name:
            raise ValueError('The user must have a first name.')
        if not last_name:
            raise ValueError('The user must have a last name.')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=is_active,
                          is_superuser=is_superuser,
                          date_joined=timezone.now(),is_complete=is_complete)
        user.first_name=first_name
        user.last_name=last_name
        user.user_type=user_type
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email,first_name,last_name, password, user_type,is_staff=False,
    is_active=True,is_complete=True):
        return self._create_user(email,first_name,last_name,password, is_staff, False,
        user_type,is_active,is_complete)

    def create_superuser(self, email, password,first_name,last_name):
        return self._create_user(email,first_name,last_name,password, is_staff=True,
         is_superuser=True,user_type=self.model.Types.SUPERUSER,is_active=True,is_complete=True)

class User(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.

    Email, first_name, last_name and password are required. Other fields are optional.
    """
    class Types(models.TextChoices):
        SUPERUSER = "SUPERUSER",_("Superuser")
        ADMINISTRATOR = "ADMINISTRATOR",_("Administator")
        TEACHER = "TEACHER",_("Teacher")
        STUDENT = "STUDENT",_("Student")
    id = models.BigAutoField(_('id'), primary_key=True)
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=False, null=False)
    last_name = models.CharField(_('last name'), max_length=30, blank=False,null=False)
    user_type = models.CharField(max_length=40,choices=Types.choices,default=Types.STUDENT,
        help_text=_('Determines the type of user this is.'))
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    is_complete = models.BooleanField(_('is complete'),default=True,
        help_text=_('Designates whether this user\'s data is complete.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        """
        Returns the last_name plus the first_name , with a space in between.
        """
        full_name = '%s %s' % (self.last_name, self.first_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.last_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

class Teacher(models.Model):
    """
        Represents a teacher with their user data, their grade and the sections they teach.
    """
    class Grades(models.TextChoices):
        MAB = "MAB","MAB"
        MAA = "MAA","MAA"
        MCB = "MCB","MCB"
        MCA = "MCA","MCA"
        PR = "PR","Pr"
        DOC = "DOC","Doc"

    user = models.OneToOneField('User', verbose_name=_('user'), primary_key=True, on_delete=models.CASCADE)
    grade = models.CharField(_('grade'), max_length=10, choices=Grades.choices, blank=False)
    sections = models.ManyToManyField('Management.Section', verbose_name=_('sections'),through='Management.TeacherSection')

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = _('Teacher')
        verbose_name_plural = _('Teachers')

class Student(models.Model):
    """
        Represents a student with their user data, their registration number and the section they belong to.
    """
    #TODO:Add group field.
    user = models.OneToOneField('User', verbose_name=_('user'), primary_key=True, on_delete=models.CASCADE)
    section = models.ForeignKey('Management.Section', verbose_name=_('section'), on_delete=models.CASCADE)
    group = models.PositiveSmallIntegerField(_('group'))
    registration_number = models.CharField(_('registration number'), max_length=20)

#Uncomment this when needing to add extra data to the admin users.
#(obviously gonna have to handle this extra data yourself if you add any.)
#class Admin(models.Model):
#    """
#        Represents an admin with their user data...
#    """
#    user = models.OneToOneField('user', verbose_name=_('user'), primary_key=True, on_delete=models.CASCADE)
