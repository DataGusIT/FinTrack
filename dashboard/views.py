from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from expenses.models import Transaction, Category
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

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'recent_transactions': transactions[:5],
        'category_labels': category_labels,
        'category_data': category_data,
    }
    
    return render(request, 'dashboard/index.html', context)