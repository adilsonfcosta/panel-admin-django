from django import forms
from .models import Organization, Company


class OrganizationForm(forms.ModelForm):
    """
    Formulário para criação e edição de organizações.
    """
    is_active = forms.BooleanField(
        required=False,
        label='Ativa',
        widget=forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-blue-600 focus:ring-blue-600 border-gray-400 rounded'})
    )
    
    class Meta:
        model = Organization
        fields = ('name', 'description', 'is_active')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'shadow-sm focus:ring-blue-600 focus:border-blue-600 block w-full text-base border-gray-400 rounded-md bg-white text-gray-900'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'shadow-sm focus:ring-blue-600 focus:border-blue-600 block w-full text-base border-gray-400 rounded-md bg-white text-gray-900'}),
        }


class CompanyForm(forms.ModelForm):
    """
    Formulário para criação e edição de empresas.
    """
    is_active = forms.BooleanField(
        required=False,
        label='Ativa',
        widget=forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-blue-600 focus:ring-blue-600 border-gray-400 rounded'})
    )
    
    class Meta:
        model = Company
        fields = ('name', 'description', 'is_active')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'shadow-sm focus:ring-blue-600 focus:border-blue-600 block w-full text-base border-gray-400 rounded-md bg-white text-gray-900'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'shadow-sm focus:ring-blue-600 focus:border-blue-600 block w-full text-base border-gray-400 rounded-md bg-white text-gray-900'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.organization and not instance.pk:  # Se for uma nova empresa
            instance.organization = self.organization
        if commit:
            instance.save()
        return instance