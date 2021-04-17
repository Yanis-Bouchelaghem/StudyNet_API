from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class Homework(models.Model):
    """
        Represents a homework with 
    """
    id = models.BigAutoField(_("id"), primary_key=True)
    assignment = models.ForeignKey("Management.Assignment", verbose_name=_("assignment"), on_delete=models.CASCADE)
    concerned_groups = ArrayField(base_field=models.PositiveSmallIntegerField())
    title = models.CharField(_("title"), max_length=150)
    due_date = models.DateTimeField(_("due date"), auto_now=False, auto_now_add=False)
    comment = models.TextField(_("comment"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Homework')
        verbose_name_plural = _('Homeworks')
