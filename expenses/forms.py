from django import forms
from .models import Transaction, Category, Budget, PaymentMethod

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['description', 'amount', 'date', 'type', 'category', 'payment_method', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full p-2 border rounded'}),
            'description': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Ex: Supermercado'}),
            'amount': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded', 'step': '0.01'}),
            'type': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'category': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'payment_method': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'status': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type', 'color', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Ex: Moradia'}),
            'type': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'color': forms.TextInput(attrs={'type': 'color', 'class': 'w-full h-10 p-1 border rounded'}),
            'icon': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'fa-home'}),
        }

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount', 'month', 'year']
        widgets = {
            'category': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'amount': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded', 'step': '0.01'}),
            'month': forms.Select(choices=[(i, i) for i in range(1, 13)], attrs={'class': 'w-full p-2 border rounded'}),
            'year': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Mostra apenas categorias do tipo DESPESA para orçamento
            self.fields['category'].queryset = Category.objects.filter(user=user, type='EXPENSE')

class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ['name', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Ex: Banco Inter'}),
            'type': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
        }