from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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