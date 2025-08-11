from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User
from organizations.models import Company
from .forms import CustomUserCreationForm, CustomUserChangeForm, GroupForm

# Views para gerenciamento de usuários

@login_required
@permission_required('accounts.view_user', raise_exception=True)
def user_list(request):
    """
    Lista todos os usuários do sistema, filtrados de acordo com as permissões do usuário logado.
    """
    user = request.user
    
    if user.is_superuser:
        # Superusuário vê todos os usuários
        users = User.objects.all().order_by('username')
    elif user.has_perm('accounts.view_all_users') and user.company and user.company.organization:
        # Administrador da Organização vê usuários da sua organização
        users = User.objects.filter(
            Q(company__organization=user.company.organization) | 
            Q(company__isnull=True, is_superuser=True)
        ).order_by('username')
    elif user.has_perm('accounts.view_company_users') and user.company:
        # Gerente da Empresa vê usuários da sua empresa
        users = User.objects.filter(company=user.company).order_by('username')
    else:
        # Usuário comum vê apenas seu próprio usuário
        users = User.objects.filter(pk=user.pk)
    
    # Busca
    q = request.GET.get('q', '').strip()
    if q:
        users = users.filter(
            Q(username__icontains=q) | 
            Q(first_name__icontains=q) | 
            Q(last_name__icontains=q) |
            Q(email__icontains=q)
        )
    
    context = {'users': users, 'q': q}
    
    if request.htmx:
        return HttpResponse(render_to_string('accounts/partials/user_list.html', context))
    
    return render(request, 'accounts/user_list.html', context)

@login_required
@permission_required('accounts.add_user', raise_exception=True)
def user_create(request):
    """
    Cria um novo usuário no sistema.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, user=request.user)
        if form.is_valid():
            user = form.save()
            
            # Adiciona o usuário aos grupos selecionados
            if form.cleaned_data.get('groups'):
                user.groups.set(form.cleaned_data['groups'])
            
            # Define a empresa do usuário
            if form.cleaned_data.get('company'):
                user.company = form.cleaned_data['company']
                user.save()
            
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('accounts:user_list')
    else:
        form = CustomUserCreationForm(user=request.user)
    
    return render(request, 'accounts/user_form.html', {'form': form, 'is_create': True})

@login_required
@permission_required('accounts.change_user', raise_exception=True)
def user_edit(request, pk):
    """
    Edita um usuário existente.
    """
    user = get_object_or_404(User, pk=pk)
    
    # Verifica se o usuário tem permissão para editar este usuário específico
    if not request.user.is_superuser:
        if request.user.has_perm('accounts.change_organization_users'):
            # Administrador da Organização só pode editar usuários da sua organização
            if not (user.company and user.company.organization == request.user.company.organization):
                messages.error(request, 'Você não tem permissão para editar este usuário.')
                return redirect('accounts:user_list')
        elif request.user.has_perm('accounts.change_company_users'):
            # Gerente da Empresa só pode editar usuários da sua empresa
            if user.company != request.user.company:
                messages.error(request, 'Você não tem permissão para editar este usuário.')
                return redirect('accounts:user_list')
        else:
            # Usuário comum só pode editar seu próprio usuário
            if user.pk != request.user.pk:
                messages.error(request, 'Você não tem permissão para editar este usuário.')
                return redirect('accounts:user_list')
    
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user, user=request.user)
        if form.is_valid():
            user = form.save()
            
            # Atualiza os grupos do usuário
            if form.cleaned_data.get('groups'):
                user.groups.set(form.cleaned_data['groups'])
            else:
                user.groups.clear()
            
            # Atualiza a empresa do usuário
            user.company = form.cleaned_data.get('company')
            user.save()
            
            messages.success(request, 'Usuário atualizado com sucesso!')
            return redirect('accounts:user_list')
    else:
        initial_data = {
            'groups': user.groups.all(),
        }
        form = CustomUserChangeForm(instance=user, initial=initial_data, user=request.user)
    
    return render(request, 'accounts/user_form.html', {'form': form, 'user_obj': user, 'is_create': False})

@login_required
@permission_required('accounts.delete_user', raise_exception=True)
def user_delete(request, pk):
    """
    Desativa um usuário (não exclui do banco de dados).
    """
    user = get_object_or_404(User, pk=pk)
    
    # Verifica se o usuário tem permissão para desativar este usuário específico
    if not request.user.is_superuser:
        if request.user.has_perm('accounts.delete_organization_users'):
            # Administrador da Organização só pode desativar usuários da sua organização
            if not (user.company and user.company.organization == request.user.company.organization):
                messages.error(request, 'Você não tem permissão para desativar este usuário.')
                return redirect('accounts:user_list')
        elif request.user.has_perm('accounts.delete_company_users'):
            # Gerente da Empresa só pode desativar usuários da sua empresa
            if user.company != request.user.company:
                messages.error(request, 'Você não tem permissão para desativar este usuário.')
                return redirect('accounts:user_list')
        else:
            messages.error(request, 'Você não tem permissão para desativar usuários.')
            return redirect('accounts:user_list')
    
    # Não permite desativar o próprio usuário
    if user == request.user:
        messages.error(request, 'Você não pode desativar seu próprio usuário.')
        return redirect('accounts:user_list')
    
    # Não permite desativar superusuários (a menos que seja um superusuário)
    if user.is_superuser and not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para desativar um superusuário.')
        return redirect('accounts:user_list')
    
    if request.method == 'POST':
        user.is_active = False
        user.save()
        messages.success(request, f'Usuário {user.username} desativado com sucesso!')
        return redirect('accounts:user_list')
    
    return render(request, 'accounts/user_confirm_delete.html', {'user_obj': user})

# Views para gerenciamento de grupos

@login_required
@permission_required('auth.view_group', raise_exception=True)
def group_list(request):
    """
    Lista todos os grupos de permissões.
    """
    groups = Group.objects.all()
    context = {'groups': groups}
    
    if request.htmx:
        return HttpResponse(render_to_string('accounts/partials/group_list.html', context))
    
    return render(request, 'accounts/group_list.html', context)

@login_required
@permission_required('auth.add_group', raise_exception=True)
def group_create(request):
    """
    Cria um novo grupo de permissões.
    """
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f'Grupo "{group.name}" criado com sucesso!')
            return redirect('accounts:group_list')
    else:
        form = GroupForm()
    
    return render(request, 'accounts/group_form.html', {'form': form})

@login_required
@permission_required('auth.change_group', raise_exception=True)
def group_edit(request, pk):
    """
    Edita um grupo de permissões existente.
    """
    group = get_object_or_404(Group, pk=pk)
    
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            group = form.save()
            messages.success(request, f'Grupo "{group.name}" atualizado com sucesso!')
            return redirect('accounts:group_list')
    else:
        form = GroupForm(instance=group)
    
    return render(request, 'accounts/group_form.html', {'form': form, 'group': group})

@login_required
@permission_required('auth.delete_group', raise_exception=True)
def group_delete(request, pk):
    """
    Exclui um grupo de permissões.
    """
    group = get_object_or_404(Group, pk=pk)
    
    if request.method == 'POST':
        group.delete()
        messages.success(request, f'Grupo "{group.name}" excluído com sucesso!')
        return redirect('accounts:group_list')
    
    return render(request, 'accounts/group_confirm_delete.html', {'group': group})

# Views para perfil do usuário

@login_required
def profile(request):
    """
    Exibe o perfil do usuário logado.
    """
    return render(request, 'accounts/profile.html', {'user': request.user})

# Views para alteração de senha

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """
    View personalizada para alteração de senha.
    """
    template_name = 'accounts/password_change_form.html'
    success_url = reverse_lazy('accounts:password_change_done')

@login_required
def password_change_done(request):
    """
    Página de confirmação após alteração de senha.
    """
    return render(request, 'accounts/password_change_done.html')