from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from expenses.models import Transaction, Category, Budget
from django.db.models import Sum
from datetime import datetime

@login_required
def index(request):
    # Obtém o mês e ano atual
    today = datetime.now()
    
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
        
        # Calcula porcentagem
        percent = (spent / budget.amount) * 100 if budget.amount > 0 else 0
        
        budget_data.append({
            'category': budget.category.name,
            'limit': budget.amount,
            'spent': spent,
            'percent': min(percent, 100), # Capar em 100 para a barra não quebrar
            'is_over': percent > 100,
            'color': budget.category.color
        })

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'recent_transactions': transactions[:5],
        'category_labels': category_labels,
        'category_data': category_data,
        'budget_data': budget_data,
    }
    
    return render(request, 'dashboard/index.html', context)