# Painel Administrativo Django

Sistema de painel administrativo desenvolvido em Django com interface moderna usando TailwindCSS e HTMX.

## Características

- Sistema de autenticação e autorização
- Gestão de organizações e empresas
- Gestão de usuários e grupos
- Interface responsiva com TailwindCSS
- Interações dinâmicas com HTMX
- Dashboard com estatísticas

## Tecnologias

- Python 3.11
- Django 4.2
- PostgreSQL/MariaDB/MySQL
- TailwindCSS
- HTMX
- Axios

## Estrutura do Projeto

- `accounts/` - App para gestão de usuários e autenticação
- `organizations/` - App para gestão de organizações e empresas
- `core/` - App principal com dashboard e funcionalidades centrais
- `templates/` - Templates HTML do sistema

## Instalação

1. Clone o repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Configure o banco de dados
4. Execute as migrações: `python manage.py migrate`
5. Crie um superusuário: `python manage.py createsuperuser`
6. Execute o servidor: `python manage.py runserver`