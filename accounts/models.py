from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from organizations.models import Company


class User(AbstractUser):
    """
    Modelo de usuário personalizado que estende o AbstractUser do Django.
    Adiciona campos específicos para o sistema de gestão.
    """
    email = models.EmailField(_('email address'), unique=True)
    is_active = models.BooleanField(default=True)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='users',
        verbose_name=_('company'),
        null=True,
        blank=True
    )
    
    # Campos adicionais podem ser adicionados conforme necessário
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        
    def __str__(self):
        return self.email