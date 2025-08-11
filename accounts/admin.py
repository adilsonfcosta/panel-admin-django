from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Configuração do admin para o modelo User personalizado.
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'company', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'company__organization')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('company',)}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {'fields': ('email', 'company')}),
    )