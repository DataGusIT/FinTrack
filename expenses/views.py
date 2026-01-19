from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Transaction
from .forms import TransactionForm

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