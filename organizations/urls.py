from django.urls import path
from . import views

app_name = 'organizations'

urlpatterns = [
    # Gerenciamento de organizações
    path('', views.organization_list, name='organization_list'),
    path('create/', views.organization_create, name='organization_create'),
    path('<int:pk>/edit/', views.organization_edit, name='organization_edit'),
    path('<int:pk>/delete/', views.organization_delete, name='organization_delete'),
    
    # Gerenciamento de empresas
    path('<int:org_pk>/companies/', views.company_list, name='company_list'),
    path('<int:org_pk>/companies/create/', views.company_create, name='company_create'),
    path('<int:org_pk>/companies/<int:pk>/edit/', views.company_edit, name='company_edit'),
    path('<int:org_pk>/companies/<int:pk>/delete/', views.company_delete, name='company_delete'),
]