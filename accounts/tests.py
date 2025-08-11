from django.test import TestCase
from django.contrib.auth import get_user_model
from organizations.models import Organization, Company

User = get_user_model()


class UserModelTest(TestCase):
    """
    Testes para o modelo User personalizado.
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
    
    def test_create_user(self):
        """
        Testa a criação de um usuário.
        """
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            company=self.company
        )
        
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.company, self.company)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_superuser(self):
        """
        Testa a criação de um superusuário.
        """
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        
        self.assertEqual(admin_user.username, 'admin')
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
    
    def test_user_str_representation(self):
        """
        Testa a representação string do usuário.
        """
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.assertEqual(str(user), 'test@example.com')