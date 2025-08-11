from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .models import Organization, Company
from .forms import OrganizationForm, CompanyForm

# Views para gerenciamento de organizações

@login_required
@permission_required('organizations.view_organization', raise_exception=True)
def organization_list(request):
    """
    Lista todas as organizações, filtradas de acordo com as permissões do usuário logado.
    """
    if request.user.is_superuser:
        # Administrador Master vê todas as organizações
        organizations = Organization.objects.all()
    elif request.user.groups.filter(name='Administrador da Organização').exists() and request.user.company:
        # Administrador da Organização vê apenas sua organização
        organizations = Organization.objects.filter(pk=request.user.company.organization.pk)
    else:
        # Outros usuários não têm acesso a esta view (será bloqueado pelo permission_required)
        organizations = Organization.objects.none()
    
    # Busca
    q = request.GET.get('q', '').strip()
    if q:
        organizations = organizations.filter(Q(name__icontains=q) | Q(description__icontains=q))
    
    # Paginação
    paginator = Paginator(organizations.order_by('name'), 10)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    context = {
        'organizations': page_obj,
        'page_obj': page_obj,
        'paginator': paginator,
        'q': q,
    }
    
    if request.htmx:
        return HttpResponse(render_to_string('organizations/partials/organization_list.html', context))
    
    return render(request, 'organizations/organization_list.html', context)

@login_required
@permission_required('organizations.add_organization', raise_exception=True)
def organization_create(request):
    """
    Cria uma nova organização.
    """
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            organization = form.save()
            messages.success(request, f'Organização "{organization.name}" criada com sucesso!')
            return redirect('organizations:organization_list')
    else:
        form = OrganizationForm()
    
    return render(request, 'organizations/organization_form.html', {'form': form})

@login_required
@permission_required('organizations.change_organization', raise_exception=True)
def organization_edit(request, pk):
    """
    Edita uma organização existente.
    """
    organization = get_object_or_404(Organization, pk=pk)
    
    # Verifica se o usuário tem permissão para editar esta organização específica
    if not request.user.is_superuser and (not request.user.company or request.user.company.organization.pk != organization.pk):
        messages.error(request, 'Você não tem permissão para editar esta organização.')
        return redirect('organizations:organization_list')
    
    if request.method == 'POST':
        form = OrganizationForm(request.POST, instance=organization)
        if form.is_valid():
            organization = form.save()
            messages.success(request, f'Organização "{organization.name}" atualizada com sucesso!')
            return redirect('organizations:organization_list')
    else:
        form = OrganizationForm(instance=organization)
    
    return render(request, 'organizations/organization_form.html', {'form': form, 'organization': organization})

@login_required
@permission_required('organizations.delete_organization', raise_exception=True)
def organization_delete(request, pk):
    """
    Desativa uma organização (não exclui do banco de dados).
    """
    organization = get_object_or_404(Organization, pk=pk)
    
    # Verifica se o usuário tem permissão para desativar esta organização específica
    if not request.user.is_superuser:
        messages.error(request, 'Apenas o Administrador Master pode desativar organizações.')
        return redirect('organizations:organization_list')
    
    if request.method == 'POST':
        organization.is_active = False
        organization.save()
        messages.success(request, f'Organização "{organization.name}" foi desativada com sucesso!')
        return redirect('organizations:organization_list')
    
    return render(request, 'organizations/organization_confirm_delete.html', {'organization': organization})

# Views para gerenciamento de empresas

@login_required
@permission_required('organizations.view_company', raise_exception=True)
def company_list(request, org_pk):
    """
    Lista todas as empresas de uma organização específica.
    """
    organization = get_object_or_404(Organization, pk=org_pk)
    
    # Verifica se o usuário tem permissão para ver as empresas desta organização
    if not request.user.is_superuser and (not request.user.company or request.user.company.organization.pk != organization.pk):
        messages.error(request, 'Você não tem permissão para ver as empresas desta organização.')
        return redirect('organizations:organization_list')
    
    companies = Company.objects.filter(organization=organization)
    
    # Busca
    q = request.GET.get('q', '').strip()
    if q:
        companies = companies.filter(Q(name__icontains=q) | Q(description__icontains=q))
    
    # Paginação
    paginator = Paginator(companies.order_by('name'), 10)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    context = {
        'organization': organization,
        'companies': page_obj,
        'page_obj': page_obj,
        'paginator': paginator,
        'q': q,
    }
    
    if request.htmx:
        return HttpResponse(render_to_string('organizations/partials/company_list.html', context))
    
    return render(request, 'organizations/company_list.html', context)

@login_required
@permission_required('organizations.add_company', raise_exception=True)
def company_create(request, org_pk):
    """
    Cria uma nova empresa em uma organização específica.
    """
    organization = get_object_or_404(Organization, pk=org_pk)
    
    # Verifica se o usuário tem permissão para adicionar empresas a esta organização
    if not request.user.is_superuser and (not request.user.company or request.user.company.organization.pk != organization.pk):
        messages.error(request, 'Você não tem permissão para adicionar empresas a esta organização.')
        return redirect('organizations:organization_list')
    
    if request.method == 'POST':
        form = CompanyForm(request.POST, organization=organization)
        if form.is_valid():
            company = form.save()
            messages.success(request, f'Empresa "{company.name}" criada com sucesso!')
            return redirect('organizations:company_list', org_pk=organization.pk)
    else:
        form = CompanyForm(organization=organization)
    
    return render(request, 'organizations/company_form.html', {'organization': organization, 'form': form})

@login_required
@permission_required('organizations.change_company', raise_exception=True)
def company_edit(request, org_pk, pk):
    """
    Edita uma empresa existente.
    """
    organization = get_object_or_404(Organization, pk=org_pk)
    company = get_object_or_404(Company, pk=pk, organization=organization)
    
    # Verifica se o usuário tem permissão para editar esta empresa específica
    if not request.user.is_superuser and (not request.user.company or request.user.company.organization.pk != organization.pk):
        messages.error(request, 'Você não tem permissão para editar empresas desta organização.')
        return redirect('organizations:organization_list')
    
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company, organization=organization)
        if form.is_valid():
            company = form.save()
            messages.success(request, f'Empresa "{company.name}" atualizada com sucesso!')
            return redirect('organizations:company_list', org_pk=organization.pk)
    else:
        form = CompanyForm(instance=company, organization=organization)
    
    return render(request, 'organizations/company_form.html', {
        'organization': organization, 
        'form': form, 
        'company': company
    })

@login_required
@permission_required('organizations.delete_company', raise_exception=True)
def company_delete(request, org_pk, pk):
    """
    Desativa uma empresa (não exclui do banco de dados).
    """
    organization = get_object_or_404(Organization, pk=org_pk)
    company = get_object_or_404(Company, pk=pk, organization=organization)
    
    # Verifica se o usuário tem permissão para desativar esta empresa específica
    if not request.user.is_superuser and (not request.user.company or request.user.company.organization.pk != organization.pk):
        messages.error(request, 'Você não tem permissão para desativar empresas desta organização.')
        return redirect('organizations:organization_list')
    
    if request.method == 'POST':
        company.is_active = False
        company.save()
        messages.success(request, f'Empresa "{company.name}" foi desativada com sucesso!')
        return redirect('organizations:company_list', org_pk=organization.pk)
    
    return render(request, 'organizations/company_confirm_delete.html', {
        'organization': organization, 
        'company': company
    })