from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Transaction, Category, Budget, RecurringTransaction
from .forms import TransactionForm, CategoryForm, BudgetForm, RecurringTransactionForm
from .utils import generate_recurring_transactions
from django.db.models import Q, Count, Sum
import csv
from django.http import HttpResponse
from datetime import datetime 

@login_required
def transaction_create(request):
    if request.method == 'POST':
        # Passa o request.POST e o usuário para o formulário
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('dashboard:index')
    else:
        form = TransactionForm(user=request.user)
    
    return render(request, 'expenses/transaction_form.html', {'form': form})

@login_required
def transaction_update(request, pk):
    # Garante que o usuário só edite transações dele
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard:index')
    else:
        form = TransactionForm(instance=transaction, user=request.user)
    
    return render(request, 'expenses/transaction_form.html', {'form': form, 'is_edit': True})

@login_required
def transaction_delete(request, pk):
    # Garante que o usuário só delete transações dele
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    
    if request.method == 'POST':
        transaction.delete()
        return redirect('dashboard:index')
    
    return render(request, 'expenses/transaction_confirm_delete.html', {'transaction': transaction})

@login_required
def transaction_list(request):
    # Base: todas as transações do usuário
    transactions = Transaction.objects.filter(user=request.user)

    # Capturando filtros do GET
    search_query = request.GET.get('search')
    category_id = request.GET.get('category')
    transaction_type = request.GET.get('type')
    status = request.GET.get('status')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Aplicando os filtros se eles existirem
    if search_query:
        transactions = transactions.filter(description__icontains=search_query)
    
    if category_id:
        transactions = transactions.filter(category_id=category_id)
        
    if transaction_type:
        transactions = transactions.filter(type=transaction_type)
        
    if status:
        transactions = transactions.filter(status=status)
        
    if start_date:
        transactions = transactions.filter(date__gte=start_date)
        
    if end_date:
        transactions = transactions.filter(date__lte=end_date)

    # Dados para popular os selects do filtro
    categories = Category.objects.filter(user=request.user)
    
    context = {
        'transactions': transactions,
        'categories': categories,
        'filter_data': request.GET, # Para manter os campos preenchidos após filtrar
    }
    return render(request, 'expenses/transaction_list.html', context)

# --- VIEWS DE CATEGORIA ---

from django.db.models import Count, Sum

@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user).annotate(
        transaction_count=Count('transactions'),
        total_amount=Sum('transactions__amount')
    ).order_by('name')
    
    return render(request, 'expenses/category_list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('expenses:category_list')
    else:
        form = CategoryForm()
    return render(request, 'expenses/category_form.html', {'form': form})

@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('expenses:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'expenses/category_form.html', {'form': form, 'is_edit': True})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        category.delete()
        return redirect('expenses:category_list')
    return render(request, 'expenses/category_confirm_delete.html', {'category': category})

@login_required
def budget_list(request):
    # Buscamos todos os orçamentos do usuário
    budgets_query = Budget.objects.filter(user=request.user).order_by('-year', '-month')
    
    enhanced_budgets = []
    
    for b in budgets_query:
        # Soma os gastos REAIS para aquela categoria no mês/ano do orçamento
        spent = Transaction.objects.filter(
            user=request.user,
            category=b.category,
            type='EXPENSE',
            date__month=b.month,
            date__year=b.year
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Cálculos de progresso
        spent_float = float(spent)
        limit_float = float(b.amount)
        percent = (spent_float / limit_float) * 100 if limit_float > 0 else 0
        remaining = limit_float - spent_float
        
        enhanced_budgets.append({
            'id': b.id,
            'category': b.category,
            'month': b.month,
            'year': b.year,
            'amount': b.amount,
            'spent': spent_float,
            'percent': min(percent, 100), # Para a barra não quebrar
            'real_percent': percent,
            'remaining': max(remaining, 0),
            'is_over': percent > 100,
        })
        
    return render(request, 'expenses/budget_list.html', {'budgets': enhanced_budgets})

@login_required
def budget_create(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST, user=request.user)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('expenses:budget_list')
    else:
        from datetime import datetime
        # Pré-preenche com mês e ano atual
        form = BudgetForm(user=request.user, initial={'month': datetime.now().month, 'year': datetime.now().year})
    return render(request, 'expenses/budget_form.html', {'form': form})

@login_required
def budget_update(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('expenses:budget_list')
    else:
        form = BudgetForm(instance=budget, user=request.user)
    return render(request, 'expenses/budget_form.html', {'form': form, 'is_edit': True})

@login_required
def budget_delete(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        budget.delete()
        return redirect('expenses:budget_list')
    return render(request, 'expenses/budget_confirm_delete.html', {'budget': budget})

@login_required
def recurring_list(request):
    # Antes de listar, processamos as automações para garantir dados atualizados
    generate_recurring_transactions() 
    
    recurrences = RecurringTransaction.objects.filter(user=request.user)
    return render(request, 'expenses/recurring_list.html', {'recurrences': recurrences})

@login_required
def recurring_create(request):
    if request.method == 'POST':
        form = RecurringTransactionForm(request.POST, user=request.user)
        if form.is_valid():
            rec = form.save(commit=False)
            rec.user = request.user
            rec.save()
            
            # Gera as transações retroativas se a data de início já passou
            generate_recurring_transactions()
            
            return redirect('expenses:recurring_list')
    else:
        form = RecurringTransactionForm(user=request.user)
    return render(request, 'expenses/recurring_form.html', {'form': form})

@login_required
def export_transactions_csv(request):
    # 1. Pegamos os dados filtrados (reutilizando a lógica da listagem)
    transactions = Transaction.objects.filter(user=request.user)

    # Aplicar os mesmos filtros do request.GET
    search = request.GET.get('search')
    category = request.GET.get('category')
    t_type = request.GET.get('type')
    status = request.GET.get('status')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if search: transactions = transactions.filter(description__icontains=search)
    if category: transactions = transactions.filter(category_id=category)
    if t_type: transactions = transactions.filter(type=t_type)
    if status: transactions = transactions.filter(status=status)
    if start_date: transactions = transactions.filter(date__gte=start_date)
    if end_date: transactions = transactions.filter(date__lte=end_date)

    # 2. Configurar a resposta do navegador para download de arquivo
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="extrato_fintrack_{datetime.now().strftime("%Y%m%d")}.csv"'
    # Garantir suporte a caracteres brasileiros no Excel
    response.write(u'\ufeff'.encode('utf8')) 

    writer = csv.writer(response, delimiter=';')
    
    # Cabeçalho do Excel
    writer.writerow(['Data', 'Descrição', 'Categoria', 'Tipo', 'Valor', 'Status', 'Método'])

    # Dados
    for tx in transactions:
        writer.writerow([
            tx.date.strftime("%d/%m/%Y"),
            tx.description,
            tx.category.name if tx.category else 'Sem Categoria',
            tx.get_type_display(),
            tx.amount,
            tx.get_status_display(),
            tx.get_payment_method_display()
        ])

    return response