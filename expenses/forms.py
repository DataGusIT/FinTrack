from django import forms
from .models import Transaction, Category

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['description', 'amount', 'date', 'type', 'category', 'is_paid']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full p-2 border rounded'}),
            'description': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Ex: Supermercado'}),
            'amount': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded', 'step': '0.01'}),
            'type': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'category': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'is_paid': forms.CheckboxInput(attrs={'class': 'mr-2'}),
        }

    def __init__(self, *args, **kwargs):
        # Recebe o usuário logado para filtrar as categorias
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)