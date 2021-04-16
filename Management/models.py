from django.db import models
from utilities import ChoiceArrayField
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class Department(models.Model):
    """
        Represents a department with a code and a name.
    """
    code = models.CharField(_('code'),max_length=30,primary_key=True,blank=False,
        help_text=_('A code that uniquely identifies this section.'))
    name = models.CharField(_('name'),max_length=80,blank=False,
        help_text=_('A human friendly name.'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')

class Specialty(models.Model):
    """
        Represents a specialty with a code, name and the department to which it belongs.
    """
    code = models.CharField(_('code'), max_length=30,primary_key=True,blank=False,
        help_text=_('A code that uniquely identifies this specialty.'))
    name = models.CharField(_('name'),max_length=80,blank=False,
        help_text=_('A human friendly name.'))
    Department = models.ForeignKey('Department', verbose_name=_('Department'), on_delete=models.CASCADE)

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = _('Specialty')
        verbose_name_plural = _('Specialties')

class Section(models.Model):
    """
        Represents a section with a code, number of groups and the specialty to which it belongs.
    """
    code = models.CharField(_('code'), max_length=30,primary_key=True,blank=False,
        help_text=_('A code that uniquely identifies this section.'))
    number_of_groups = models.IntegerField(_('number of groups'),
        help_text=_('The number of groups this section is divided into.'))
    specialty = models.ForeignKey('Specialty', verbose_name=_('specialty'), on_delete=models.CASCADE)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')


class Module(models.Model):
    """
        Represents a module with a code, a name and the types of sessions it can have.
    """
    class Types(models.TextChoices):
        LECTURE = "LECTURE",_("Lecture")
        DIRECTED_STUDIES = "DIRECTED", _("Directed studies")
        PRACTICAL_WORK = "PRACTICAL",_("Practical work")

    code = models.CharField(_("code"),primary_key=True, max_length=30, blank=False)
    name = models.CharField(_("name"), max_length=80, blank=False)
    types= ChoiceArrayField(base_field=models.CharField(choices=Types.choices, max_length=15),
        verbose_name=_('types'),default=list)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Module')
        verbose_name_plural = _('Modules')
