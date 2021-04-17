from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _
# Create your models here.
class Session(models.Model):
    """
        Represents a session with the assignment, the concerned groups, the day,
        the start time and end time, the meeting link and optionally the meeting number, password
        and a comment.
    """
    class DaysOfWeek(models.TextChoices):
        SUNDAY = "SUNDAY",_("Sunday")
        MONDAY = "MONDAY",_("Monday")
        TUESDAY = "TUESDAY",_("Tuesday")
        WEDNESDAY = "WEDNESDAY",_("Wednesday")
        THURSDAY = "THURSDAY",_("Thursday")
        FRIDAY = "FRIDAY",_("Friday")
        SATURDAY = "SATURDAY",_("Saturday")

    id = models.BigAutoField(_('id'), primary_key=True)
    assignment = models.ForeignKey('Management.Assignment', verbose_name=_('assignment'), on_delete=models.CASCADE)
    concerned_groups = ArrayField(base_field=models.PositiveSmallIntegerField())
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
