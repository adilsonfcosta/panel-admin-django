from django.contrib import admin
from .models import Organization, Company


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o modelo Organization.
    """
    list_display = ('name', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o modelo Company.
    """
    list_display = ('name', 'organization', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'organization', 'created_at')
    search_fields = ('name', 'description', 'organization__name')
    ordering = ('organization', 'name')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('organization')