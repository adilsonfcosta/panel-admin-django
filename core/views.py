from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from organizations.models import Organization, Company
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def dashboard(request):
    """
    Dashboard principal do sistema.
    Exibe estatísticas e links para as principais funcionalidades.
    """
    user = request.user
    context = {}
    
    # Contagem de organizações, empresas e usuários
    organization_count = Organization.objects.count()
    company_count = Company.objects.count()
    user_count = User.objects.count()
    
    # Filtra os dados com base no tipo de usuário
    if user.is_superuser:
        # Superusuário vê todas as estatísticas
        context['organization_count'] = organization_count
        context['company_count'] = company_count
        context['user_count'] = user_count
        
        # Organizações recentes
        context['recent_organizations'] = Organization.objects.all().order_by('-created_at')[:5]
        
        # Empresas recentes
        context['recent_companies'] = Company.objects.all().order_by('-created_at')[:5]
        
        # Usuários recentes
        context['recent_users'] = User.objects.all().order_by('-date_joined')[:5]
        
    elif user.has_perm('organizations.view_all_organizations') and user.company and user.company.organization:
        # Administrador da Organização vê estatísticas da sua organização
        organization = user.company.organization
        context['organization'] = organization
        context['organization_count'] = 1  # Apenas a própria organização
        context['company_count'] = Company.objects.filter(organization=organization).count()
        context['user_count'] = User.objects.filter(company__organization=organization).count()
        
        # Empresas recentes da organização
        context['recent_companies'] = Company.objects.filter(
            organization=organization
        ).order_by('-created_at')[:5]
        
        # Usuários recentes da organização
        context['recent_users'] = User.objects.filter(
            company__organization=organization
        ).order_by('-date_joined')[:5]
        
    elif user.company:
        # Gerente da Empresa vê estatísticas da sua empresa
        company = user.company
        context['organization'] = company.organization
        context['company'] = company
        context['organization_count'] = 1  # Apenas a própria organização
        context['company_count'] = 1  # Apenas a própria empresa
        context['user_count'] = User.objects.filter(company=company).count()
        
        # Usuários recentes da empresa
        context['recent_users'] = User.objects.filter(
            company=company
        ).order_by('-date_joined')[:5]
    
    return render(request, 'core/dashboard.html', context)