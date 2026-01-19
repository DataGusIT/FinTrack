from django.db import models
from django.conf import settings

class Category(models.Model):
    # Tipos de categoria
    CATEGORY_TYPES = (
        ('EXPENSE', 'Despesa'),
        ('INCOME', 'Receita'),
    )

    name = models.CharField('Nome da Categoria', max_length=100)
    type = models.CharField('Tipo', max_length=7, choices=CATEGORY_TYPES)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='categories'
    )
    icon = models.CharField('Ícone', max_length=50, blank=True, help_text="Ex: fa-shopping-cart")
    color = models.CharField('Cor', max_length=7, default='#3b82f6') # Padrão azul tailwind

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        unique_together = ('name', 'user', 'type') # Evita categorias duplicadas para o mesmo usuário

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

class PaymentMethod(models.Model):
    METHOD_TYPES = (
        ('CASH', 'Dinheiro'),
        ('DEBIT', 'Débito'),
        ('CREDIT', 'Crédito'),
        ('PIX', 'PIX'),
        ('TRANSFER', 'Transferência'),
        ('BOLETO', 'Boleto'),
    )
    name = models.CharField('Nome do Método', max_length=100) # Ex: "Cartão Inter"
    type = models.CharField('Tipo', max_length=10, choices=METHOD_TYPES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('EXPENSE', 'Despesa'),
        ('INCOME', 'Receita')
    )
    
    STATUS_CHOICES = (
        ('PENDING', 'Pendente'),
        ('PAID', 'Pago'),
        ('CANCELLED', 'Cancelado'),
    )

    # Lista de métodos de pagamento pré-definida
    PAYMENT_METHOD_CHOICES = (
        ('CASH', 'Dinheiro'),
        ('DEBIT', 'Cartão de Débito'),
        ('CREDIT', 'Cartão de Crédito'),
        ('PIX', 'PIX'),
        ('TRANSFER', 'Transferência'),
        ('BOLETO', 'Boleto'),
        ('OTHER', 'Outro'),
    )

    description = models.CharField('Descrição', max_length=255)
    amount = models.DecimalField('Valor', max_digits=15, decimal_places=2)
    date = models.DateField('Data da Transação')
    type = models.CharField('Tipo', max_length=7, choices=TRANSACTION_TYPES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='transactions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    
    # Novos campos com escolhas fixas
    status = models.CharField('Status', max_length=10, choices=STATUS_CHOICES, default='PAID')
    payment_method = models.CharField(
        'Método de Pagamento', 
        max_length=10, 
        choices=PAYMENT_METHOD_CHOICES, 
        default='CASH'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.description} - R$ {self.amount}"

class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField('Limite de Gastos', max_digits=15, decimal_places=2)
    month = models.IntegerField('Mês')
    year = models.IntegerField('Ano')

    class Meta:
        unique_together = ('user', 'category', 'month', 'year') # Um orçamento por categoria/mês
        verbose_name = 'Orçamento'
        verbose_name_plural = 'Orçamentos'

    def __str__(self):
        return f"{self.category.name} - {self.month}/{self.year}"