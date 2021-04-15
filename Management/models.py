from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class Department(models.Model):
    """
        Represents a department with a code and a name.
    """
    code = models.CharField(max_length=30,primary_key=True,blank=False,
        help_text=_('A code that uniquely identifies this section.'))
    name = models.CharField(max_length=80,blank=False,
        help_text=_('Human friendly name.'))