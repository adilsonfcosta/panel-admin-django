from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from organizations.models import Organization, Company

User = get_user_model()


class DashboardViewTest(TestCase):
    """
    Testes para a view do dashboard.
    """
    
    def setUp(self):
        self.organization = Organization.objects.create(
            name='Organização Teste',
            description='Descrição da organização teste'
        )
        self.company = Company.objects.create(
            organization=self.organization,
            name='Empresa Teste',
            description='Descrição da empresa teste'
        )
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            company=self.company
        )
    
    def test_dashboard_requires_login(self):
        """
        Testa se o dashboard requer login.
        """
        response = self.client.get(reverse('core:dashboard'))
        self.assertRedirects(response, '/accounts/login/?next=/')
    
    def test_dashboard_with_authenticated_user(self):
        """
        Testa o dashboard com usuário autenticado.
        """
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('core:dashboard'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard')
        self.assertIn('user_count', response.context)
    
    def test_dashboard_with_superuser(self):
        """
        Testa o dashboard com superusuário.
        """
        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('core:dashboard'))
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('organization_count', response.context)
        self.assertIn('company_count', response.context)
        self.assertIn('user_count', response.context)