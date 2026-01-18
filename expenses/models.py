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

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('EXPENSE', 'Despesa'),
        ('INCOME', 'Receita'),
    )

    description = models.CharField('Descrição', max_length=255)
    amount = models.DecimalField('Valor', max_digits=15, decimal_places=2)
    date = models.DateField('Data da Transação')
    type = models.CharField('Tipo', max_length=7, choices=TRANSACTION_TYPES)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='transactions'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    is_paid = models.BooleanField('Pago/Recebido', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.description} - R$ {self.amount}"