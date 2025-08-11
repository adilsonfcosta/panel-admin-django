from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Organization(models.Model):
    """
    Modelo para representar uma organização que pode conter várias empresas.
    """
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True, null=True)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('organization')
        verbose_name_plural = _('organizations')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Company(models.Model):
    """
    Modelo para representar uma empresa que pertence a uma organização.
    """
    organization = models.ForeignKey(
        Organization, 
        on_delete=models.CASCADE, 
        related_name='companies',
        verbose_name=_('organization')
    )
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True, null=True)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('company')
        verbose_name_plural = _('companies')
        ordering = ['organization', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.organization.name})"