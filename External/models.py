from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class AppVersionSupport(models.Model):
    version = models.CharField(_('version'), primary_key=True, max_length=30)
    is_supported = models.BooleanField(_('is supported'))

    def __str__(self):
        return self.version

    class Meta:
        verbose_name = _('App version support')
        verbose_name_plural = _('App versions support')
