from django.db import models
from django.contrib.postgres.fields import ArrayField
from Management.models import Module
from utilities import ActionTypes
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Homework(models.Model):
    """
        Represents a homework with the assignment, concerned groups, title, due_date and a comment
    """
    id = models.BigAutoField(_("id"), primary_key=True)
    assignment = models.ForeignKey("Management.Assignment", verbose_name=_("assignment"), on_delete=models.CASCADE)
    concerned_groups = ArrayField(base_field=models.PositiveSmallIntegerField(), verbose_name=_('concerned groups'))
    title = models.CharField(_("title"), max_length=150)
    due_date = models.DateField(_("due date"), auto_now=False, auto_now_add=False)
    due_time = models.TimeField(_("due time"), auto_now=False, auto_now_add=False)
    comment = models.TextField(_("comment"), blank=True)
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Homework')
        verbose_name_plural = _('Homeworks')

class HomeworkHistory(models.Model):
    """
        Represents an entry in the history of all homeworks, contains a copy of all the data about
        the homework with the addition of the action(Add,update,delete) date, type and author.
    """
    id = models.BigAutoField(_("id"), primary_key=True)
    teacher = models.ForeignKey("Accounts.Teacher", verbose_name=_("teacher"), on_delete=models.DO_NOTHING)
    section = models.ForeignKey("Management.Section", verbose_name=_("section"), on_delete=models.DO_NOTHING)
    module = models.ForeignKey("Management.Module", verbose_name=_("module"), on_delete=models.DO_NOTHING)
    module_type = models.CharField(_('module type'), choices=Module.Types.choices,max_length=15)
    concerned_groups = ArrayField(base_field=models.PositiveSmallIntegerField(), verbose_name=_('concerned groups'))
    title = models.CharField(_("title"), max_length=150)
    due_date = models.DateField(_("due date"), auto_now=False, auto_now_add=False)
    due_time = models.TimeField(_("due time"), auto_now=False, auto_now_add=False)
    comment = models.TextField(_("comment"),blank=True)
    action_date = models.DateTimeField(_('action date'), default=timezone.now)
    action_type = models.CharField(_('action type'), choices=ActionTypes.choices,max_length=15)
    author = models.ForeignKey('Accounts.User', verbose_name=_('author'), on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.author.last_name +' '+self.author.first_name+' - '+self.action_type+' : '+self.section.code+' '+self.module.code

    class Meta:
        verbose_name = _('Homework history')
        verbose_name_plural = _('Homeworks history')