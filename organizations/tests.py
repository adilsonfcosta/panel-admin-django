from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Organization, Company

User = get_user_model()


class OrganizationModelTest(TestCase):
    """
    Testes para o modelo Organization.
    """
    
    def test_create_organization(self):
        """
        Testa a criação de uma organização.
        """
        organization = Organization.objects.create(
            name='Organização Teste',
            description='Descrição da organização teste'
        )
        
        self.assertEqual(organization.name, 'Organização Teste')
        self.assertEqual(organization.description, 'Descrição da organização teste')
        self.assertTrue(organization.is_active)
        self.assertIsNotNone(organization.created_at)
        self.assertIsNotNone(organization.updated_at)
    
    def test_organization_str_representation(self):
        """
        Testa a representação string da organização.
        """
        organization = Organization.objects.create(
            name='Organização Teste'
        )
        
        self.assertEqual(str(organization), 'Organização Teste')


class CompanyModelTest(TestCase):
    """
    Testes para o modelo Company.
    """
    
    def setUp(self):
        self.organization = Organization.objects.create(
            name='Organização Teste',
            description='Descrição da organização teste'
        )
    
    def test_create_company(self):
        """
        Testa a criação de uma empresa.
        """
        company = Company.objects.create(
            organization=self.organization,
            name='Empresa Teste',
            description='Descrição da empresa teste'
        )
        
        self.assertEqual(company.name, 'Empresa Teste')
        self.assertEqual(company.description, 'Descrição da empresa teste')
        self.assertEqual(company.organization, self.organization)
        self.assertTrue(company.is_active)
        self.assertIsNotNone(company.created_at)
        self.assertIsNotNone(company.updated_at)
    
    def test_company_str_representation(self):
        """
        Testa a representação string da empresa.
        """
        company = Company.objects.create(
            organization=self.organization,
            name='Empresa Teste'
        )
        
        self.assertEqual(str(company), 'Empresa Teste (Organização Teste)')
    
    def test_company_organization_relationship(self):
        """
        Testa o relacionamento entre empresa e organização.
        """
        company = Company.objects.create(
            organization=self.organization,
            name='Empresa Teste'
        )
        
        # Testa o relacionamento direto
        self.assertEqual(company.organization, self.organization)
        
        # Testa o relacionamento reverso
        self.assertIn(company, self.organization.companies.all())