from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from expenses.models import Transaction, Category, Budget
from django.db.models import Sum
from datetime import datetime, date
import calendar

@login_required
def index(request):
    # Obtém o mês e ano atual
    today = datetime.now()

    last_day = calendar.monthrange(today.year, today.month)[1] 
    days_passed = today.day

    # Filtra transações do usuário no mês atual
    transactions = Transaction.objects.filter(
        user=request.user, 
        date__month=today.month, 
        date__year=today.year
    )

    # Cálculos de resumo
    total_income = transactions.filter(type='INCOME').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = transactions.filter(type='EXPENSE').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense

    # --- NOVOS INDICADORES (KPIs) ---

    # 1. Taxa de Poupança
    savings_rate = 0
    if total_income > 0:
        savings_rate = ((total_income - total_expense) / total_income) * 100

    # 2. Média Diária de Gastos
    daily_avg = float(total_expense) / days_passed if days_passed > 0 else 0

    # 3. Projeção de Gastos até o fim do mês
    projection = daily_avg * last_day

    # 4. Top 5 Maiores Gastos (Categorias)
    top_categories = transactions.filter(type='EXPENSE').values(
        'category__name', 'category__color'
    ).annotate(
        total=Sum('amount')
    ).order_by('-total')[:5]

    # --- DADOS PARA OS GRÁFICOS ---
    
    # 1. Gastos por Categoria (Gráfico de Pizza)
    expenses_by_category = transactions.filter(type='EXPENSE').values('category__name').annotate(total=Sum('amount'))
    
    # Preparar listas para o JavaScript
    category_labels = [item['category__name'] for item in expenses_by_category]
    category_data = [float(item['total']) for item in expenses_by_category]

     # --- LÓGICA DE ORÇAMENTOS ---
    budgets = Budget.objects.filter(user=request.user, month=today.month, year=today.year)
    budget_data = []

    for budget in budgets:
        # Soma gastos reais dessa categoria no mês atual
        spent = Transaction.objects.filter(
            user=request.user,
            category=budget.category,
            type='EXPENSE',
            date__month=today.month,
            date__year=today.year
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Convertendo para float para evitar problemas de serialização e garantir precisão
        spent_float = float(spent)
        limit_float = float(budget.amount)

        percent = (spent_float / limit_float) * 100 if limit_float > 0 else 0

        budget_data.append({
            'category': budget.category.name,
            'limit': limit_float,
            'spent': spent_float,
            'percent': percent, # Passamos o valor real (ex: 10.0)
            'display_percent': min(percent, 100), # Para a largura da barra
            'is_over': percent > 100,
            'color': budget.category.color
        })

    # Novo Insight: Contas Pendentes
    pending_expenses = Transaction.objects.filter(
        user=request.user,
        type='EXPENSE',
        status='PENDING',
        date__month=today.month,
        date__year=today.year
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'recent_transactions': transactions[:5],
        'category_labels': category_labels,
        'category_data': category_data,
        'budget_data': budget_data,
        'pending_expenses': pending_expenses,
        'savings_rate': round(savings_rate, 1),
        'daily_avg': round(daily_avg, 2),
        'projection': round(projection, 2),
        'top_categories': top_categories,
        'days_left': last_day - days_passed,
    }
    
    return render(request, 'dashboard/index.html', context)