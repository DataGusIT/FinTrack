import random
from datetime import datetime, date
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from expenses.models import Category, Transaction, Budget, RecurringTransaction
from dateutil.relativedelta import relativedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de teste para um usuário específico'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username do usuário que receberá os dados')

    def handle(self, *args, **options):
        username = options['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Usuário "{username}" não encontrado.'))
            return

        self.stdout.write(f'Populando dados para: {user.username}...')

        # 1. CRIAR CATEGORIAS PADRÃO
        categories_data = [
            ('Alimentação', 'EXPENSE', '#ef4444', 'fa-utensils'),
            ('Transporte', 'EXPENSE', '#3b82f6', 'fa-car'),
            ('Lazer', 'EXPENSE', '#f59e0b', 'fa-gamepad'),
            ('Saúde', 'EXPENSE', '#10b981', 'fa-heartbeat'),
            ('Educação', 'EXPENSE', '#8b5cf6', 'fa-graduation-cap'),
            ('Salário', 'INCOME', '#10b981', 'fa-money-bill-wave'),
            ('Investimentos', 'INCOME', '#06b6d4', 'fa-chart-line'),
        ]

        categories = []
        for name, ctype, color, icon in categories_data:
            cat, _ = Category.objects.get_or_create(
                name=name, user=user, type=ctype,
                defaults={'color': color, 'icon': icon}
            )
            categories.append(cat)

        # 2. CRIAR ORÇAMENTOS (METAS) PARA O MÊS ATUAL
        today = date.today()
        for cat in [c for c in categories if c.type == 'EXPENSE']:
            Budget.objects.get_or_create(
                user=user, category=cat, month=today.month, year=today.year,
                defaults={'amount': Decimal(random.randrange(500, 2000, 100))}
            )

        # 3. CRIAR TRANSAÇÕES DOS ÚLTIMOS 6 MESES
        descriptions = {
            'Alimentação': ['Supermercado', 'Ifood', 'Restaurante', 'Padaria'],
            'Transporte': ['Gasolina', 'Uber', 'Manutenção Carro', 'Pedágio'],
            'Lazer': ['Cinema', 'Netflix', 'Show', 'Viagem FDS'],
            'Saúde': ['Farmácia', 'Consulta', 'Exame', 'Academia'],
            'Educação': ['Curso Online', 'Livros', 'Mensalidade', 'Workshop'],
            'Salário': ['Pagamento Mensal', 'Bônus Performance', 'Freelance'],
            'Investimentos': ['Dividendos', 'Rendimento FIIs', 'Resgate CDB'],
        }

        self.stdout.write('Gerando transações históricas...')
        
        for i in range(6): # Últimos 6 meses
            month_date = today - relativedelta(months=i)
            
            # Criar 2 Receitas por mês
            income_cats = [c for c in categories if c.type == 'INCOME']
            for _ in range(2):
                cat = random.choice(income_cats)
                Transaction.objects.create(
                    user=user,
                    category=cat,
                    description=random.choice(descriptions[cat.name]),
                    amount=Decimal(random.randrange(2000, 5000, 500)),
                    date=month_date.replace(day=random.randint(1, 5)),
                    type='INCOME',
                    status='PAID',
                    payment_method='TRANSFER'
                )

            # Criar 10-15 Despesas por mês
            expense_cats = [c for c in categories if c.type == 'EXPENSE']
            for _ in range(12):
                cat = random.choice(expense_cats)
                status = 'PAID' if month_date.month != today.month else random.choice(['PAID', 'PENDING'])
                
                Transaction.objects.create(
                    user=user,
                    category=cat,
                    description=random.choice(descriptions[cat.name]),
                    amount=Decimal(random.uniform(20, 400)).quantize(Decimal('0.00')),
                    date=month_date.replace(day=random.randint(1, 28)),
                    type='EXPENSE',
                    status=status,
                    payment_method=random.choice(['CREDIT', 'DEBIT', 'PIX', 'CASH'])
                )
        # 4. CRIAR TRANSAÇÕES RECORRENTES (ASSINATURAS)
        self.stdout.write('Gerando automações recorrentes...')
        
        recurring_data = [
            ('Assinatura Netflix', 55.90, 'Lazer', 'MONTHLY', 'CREDIT'),
            ('Academia Mensal', 120.00, 'Saúde', 'MONTHLY', 'DEBIT'),
            ('Internet Fibra', 99.90, 'Educação', 'MONTHLY', 'PIX'),
            ('Spotify Família', 34.90, 'Lazer', 'MONTHLY', 'CREDIT'),
        ]

        for desc, val, cat_name, freq, method in recurring_data:
            cat = Category.objects.get(name=cat_name, user=user)
            RecurringTransaction.objects.get_or_create(
                user=user,
                description=desc,
                defaults={
                    'amount': Decimal(val),
                    'type': 'EXPENSE',
                    'category': cat,
                    'payment_method': method,
                    'frequency': freq,
                    'start_date': today.replace(day=1),
                    'is_active': True
                }
            )

        self.stdout.write(self.style.SUCCESS('Banco de dados e Automações populados!'))

        self.stdout.write(self.style.SUCCESS('Banco de dados populado com sucesso!'))