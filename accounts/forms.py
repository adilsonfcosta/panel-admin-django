from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from organizations.models import Company
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Formulário para criação de usuários com campos personalizados.
    """
    company = forms.ModelChoiceField(
        queryset=Company.objects.filter(is_active=True),
        required=False,
        label='Empresa',
        widget=forms.Select(attrs={'class': 'shadow-sm focus:ring-blue-600 focus:border-blue-600 block w-full text-base border-gray-400 rounded-md bg-white text-gray-900'})
    )
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        label='Grupos',
        widget=forms.SelectMultiple(attrs={'class': 'shadow-sm focus:ring-blue-600 focus:border-blue-600 block w-full text-base border-gray-400 rounded-md bg-white text-gray-900'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'company', 'groups')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'shadow-sm focus:ring-blue-600 focus:border-blue-600 block w-full text-base border-gray-400 rounded-md bg-white text-gray-900'}),
            'email': forms.EmailInput(attrs={'class': 'shadow-sm focus:ring-blue-600 focus:border-blue-600 block w-full text-base border-gray-400 rounded-md bg-white text-gray-900'}),
            'first_name': forms.TextInput(attrs={'class': 'shadow-sm focus:ring-blue-600 focus:border-blue-600 block w-full text-base border-gray-400 rounded-md bg-white text-gray-900'}),
            'last_name': forms.TextInput(attrs={'class': 'shadow-sm focus:ring-blue-600 focus:border-blue-600 block w-full text-base border-gray-400 rounded-md bg-white text-gray-900'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Torna a empresa obrigatória para criadores que não são superusuários
        if user and not user.is_superuser:
            self.fields['company'].required = True
            
        # Filtra as empresas disponíveis com base no usuário logado
        if user and not user.is_superuser and user.company:
            # Administrador da Organização vê apenas empresas da sua organização
            self.fields['company'].queryset = Company.objects.filter(
                organization=user.company.organization,
                is_active=True
            )


class CustomUserChangeForm(UserChangeForm):
    """
    Formulário para edição de usuários com campos personalizados.
    """
    company = forms.ModelChoiceField(
        queryset=Company.objects.filter(is_active=True),
        required=False,
        label='Empresa',
        widget=forms.Select(attrs={'class': 'shadow-sm focus:ring-blue-600 focus:border-blue-600 block w-full text-base border-gray-400 rounded-md bg-white text-gray-900'})
    )
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        label='Grupos',
        widget=forms.SelectMultiple(attrs={'class': 'shadow-sm focus:ring-blue-600 focus:border-blue-600 block w-full text-base border-gray-400 rounded-md bg-white text-gray-900'})
    )
    is_active = forms.BooleanField(
        required=False,
        label='Ativo',
        widget=forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-blue-600 focus:ring-blue-600 border-gray-400 rounded'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'company', 'groups', 'is_active')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'shadow-sm focus:ring-blue-600 focus:border-blue-600 block w-full text-base border-gray-400 rounded-md bg-white text-gray-900'}),
            'email': forms.EmailInput(attrs={'class': 'shadow-sm focus:ring-blue-600 focus:border-blue-600 block w-full text-base border-gray-400 rounded-md bg-white text-gray-900'}),
            'first_name': forms.TextInput(attrs={'class': 'shadow-sm focus:ring-blue-600 focus:border-blue-600 block w-full text-base border-gray-400 rounded-md bg-white text-gray-900'}),
            'last_name': forms.TextInput(attrs={'class': 'shadow-sm focus:ring-blue-600 focus:border-blue-600 block w-full text-base border-gray-400 rounded-md bg-white text-gray-900'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Remove o campo de senha do formulário de edição
        if 'password' in self.fields:
            self.fields.pop('password')
        
        # Filtra as empresas disponíveis com base no usuário logado
        if user and not user.is_superuser and user.company:
            # Administrador da Organização vê apenas empresas da sua organização
            self.fields['company'].queryset = Company.objects.filter(
                organization=user.company.organization,
                is_active=True
            )


class GroupForm(forms.ModelForm):
    """
    Formulário para criação e edição de grupos.
    """
    class Meta:
        model = Group
        fields = ('name', 'permissions')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'shadow-sm focus:ring-blue-600 focus:border-blue-600 block w-full text-base border-gray-400 rounded-md bg-white text-gray-900'}),
            'permissions': forms.CheckboxSelectMultiple(attrs={'class': 'h-5 w-5 text-blue-600 focus:ring-blue-600 border-gray-400 rounded'}),
        }