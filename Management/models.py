from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _
from utilities import ChoiceArrayField

# Create your models here.

class Department(models.Model):
    """
        Represents a department with a code and a name.
    """
    code = models.CharField(_('code'),max_length=30,primary_key=True,blank=False,
        help_text=_('A code that uniquely identifies this department.'))
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
    department = models.ForeignKey('Department', verbose_name=_('department'), on_delete=models.CASCADE)

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
    number_of_groups = models.PositiveSmallIntegerField(_('number of groups'),
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

    code = models.CharField(_('code'),primary_key=True, max_length=30, blank=False)
    name = models.CharField(_('name'), max_length=80, blank=False)
    types= ChoiceArrayField(base_field=models.CharField(choices=Types.choices, max_length=15),
        verbose_name=_('types'),default=list)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Module')
        verbose_name_plural = _('Modules')

class TeacherSection(models.Model):
    """
        The through table to represent the relation-ship between a teacher and the sections he teaches.
        (explicitly declared to be able to reference it later.)
    """
    teacher = models.ForeignKey('Accounts.Teacher', verbose_name=_('teacher'), on_delete=models.CASCADE)
    section = models.ForeignKey('Section', verbose_name=_('section'), on_delete=models.CASCADE)

    def __str__(self):
        return self.section.code + ' ; ' + self.teacher.user.email + ' (' + self.teacher.user.last_name + ' ' + self.teacher.user.first_name + ')'

    class Meta:
        verbose_name = _('Teacher-Section')
        verbose_name_plural = _('Teachers-Sections')
        constraints = [
            models.UniqueConstraint(fields=['teacher','section'], name='unique_teachers_section')
        ]

class Assignment(models.Model):
    """
        Represents which section,module and group each teacher is assigned to teach.
    """
    id = models.BigAutoField(_('id'),primary_key=True)
    teacher_section = models.ForeignKey('TeacherSection', verbose_name=_('teacher-section'), on_delete=models.CASCADE)
    module = models.ForeignKey('Module', verbose_name=_('module'), on_delete=models.CASCADE)
    module_type = models.CharField(_('module type'), choices=Module.Types.choices,max_length=15)
    concerned_groups = ArrayField(base_field=models.PositiveSmallIntegerField(), verbose_name=_('concerned groups'))
    def __str__(self):
        return self.teacher_section.teacher.user.last_name + ' ' + self.teacher_section.teacher.user.first_name + ' ; ' + self.teacher_section.section.code + ' ; ' + self.module.code + ' ; ' + dict(Module.Types.choices)[self.module_type]

    class Meta:
        verbose_name = _('Assignment')
        verbose_name_plural = _('Assignments')
        constraints = [
            models.UniqueConstraint(fields=['teacher_section','module','module_type'], name='unique_assignment')
        ]
