from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from expenses.models import Transaction, Category
from datetime import date

User = get_user_model()

class DashboardViewTests(TestCase):
    def setUp(self):
        # Criar usuário de teste
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client = Client()
        self.client.login(username='testuser', password='password123')
        
        # Criar categoria de teste
        self.category = Category.objects.create(name="Saúde", type="EXPENSE", user=self.user)

    def test_dashboard_calculations(self):
        """Verifica se a soma de receitas e despesas no dashboard está correta"""
        # Criar uma receita e uma despesa
        Transaction.objects.create(
            description="Salário", amount=5000, date=date.today(), 
            type='INCOME', user=self.user, category=self.category
        )
        Transaction.objects.create(
            description="Aluguel", amount=1500, date=date.today(), 
            type='EXPENSE', user=self.user, category=self.category
        )

        response = self.client.get(reverse('dashboard:index'))
        
        # Verifica se o status é 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Verifica se os valores no contexto da página estão certos
        self.assertEqual(response.context['total_income'], 5000)
        self.assertEqual(response.context['total_expense'], 1500)
        self.assertEqual(response.context['balance'], 3500)

    def test_dashboard_requires_login(self):
        """Verifica se usuários não logados são redirecionados"""
        self.client.logout()
        response = self.client.get(reverse('dashboard:index'))
        self.assertEqual(response.status_code, 302) # Redirecionamento para login