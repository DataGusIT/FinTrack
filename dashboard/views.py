from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from expenses.models import Transaction
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

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'recent_transactions': transactions[:5], # Últimas 5
    }
    
    return render(request, 'dashboard/index.html', context)