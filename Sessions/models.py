from django.db import models
from django.contrib.postgres.fields import ArrayField
from Management.models import Module
from utilities import ActionTypes
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
# Create your models here.
class Session(models.Model):
    """
        Represents a session with the assignment, the concerned groups, the day,
        the start time and end time, the meeting link and optionally the meeting number, password
        and a comment.
    """
    class DaysOfWeek(models.TextChoices):
        #TODO : Change days representation to ints
        SUNDAY = "SUNDAY",_("Sunday")
        MONDAY = "MONDAY",_("Monday")
        TUESDAY = "TUESDAY",_("Tuesday")
        WEDNESDAY = "WEDNESDAY",_("Wednesday")
        THURSDAY = "THURSDAY",_("Thursday")
        FRIDAY = "FRIDAY",_("Friday")
        SATURDAY = "SATURDAY",_("Saturday")

    id = models.BigAutoField(_('id'), primary_key=True)
    assignment = models.ForeignKey('Management.Assignment', verbose_name=_('assignment'), on_delete=models.CASCADE)
    concerned_groups = ArrayField(base_field=models.PositiveSmallIntegerField(), verbose_name=_('Concerned groups'))
    day = models.CharField(_('day'), choices=DaysOfWeek.choices, max_length=15)
    start_time = models.TimeField(_('start time'), auto_now=False, auto_now_add=False)
    end_time = models.TimeField(_('end time'), auto_now=False, auto_now_add=False)
    meeting_link = models.CharField(_('meeting link'), max_length=400)
    meeting_number = models.CharField(_('meeting number'), max_length=50, blank=True)
    meeting_password = models.CharField(_('meeting password'), max_length=50, blank=True)
    comment = models.TextField(_('comment'), blank=True)

    def __str__(self):
        return self.meeting_link

    class Meta:
        verbose_name = _('Session  ')
        verbose_name_plural = _('Sessions')

class SessionHistory(models.Model):
    """
        Represents an entry in the history of all sessions, contains a copy of all the data about
        the session with the addition of the action(Add,update,delete) date, type and author.

    """

    id = models.BigAutoField(_('id'), primary_key=True)
    teacher = models.ForeignKey('Accounts.Teacher', verbose_name=_('teacher'), on_delete=models.DO_NOTHING)
    section = models.ForeignKey('Management.Section', verbose_name=_('section'), on_delete=models.DO_NOTHING)
    module = models.ForeignKey('Management.Module', verbose_name=_('module'), on_delete=models.DO_NOTHING)
    module_type = models.CharField(_('module type'), choices=Module.Types.choices,max_length=15)
    concerned_groups = ArrayField(base_field=models.PositiveSmallIntegerField(), verbose_name=_('Concerned groups'))
    day = models.CharField(_('day'), choices=Session.DaysOfWeek.choices, max_length=15)
    start_time = models.TimeField(_('start time'), auto_now=False, auto_now_add=False)
    end_time = models.TimeField(_('end time'), auto_now=False, auto_now_add=False)
    meeting_link = models.CharField(_('meeting link'), max_length=400)
    meeting_number = models.CharField(_('meeting number'), max_length=50, blank=True)
    meeting_password = models.CharField(_('meeting password'), max_length=50, blank=True)
    comment = models.TextField(_('comment'), blank=True)
    action_date = models.DateTimeField(_('action date'), default=timezone.now)
    action_type = models.CharField(_('action type'), choices=ActionTypes.choices,max_length=15)
    author = models.ForeignKey('Accounts.User', verbose_name=_('author'), on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.author.last_name +' '+self.author.first_name+' - '+self.action_type+' : '+self.section.code+' '+self.module.code

    class Meta:
        verbose_name = _('Session history')
        verbose_name_plural = _('Sessions history')