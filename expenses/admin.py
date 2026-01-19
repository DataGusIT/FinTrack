from django.contrib import admin
from .models import Category, Transaction, Budget 

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'user')
    list_filter = ('type', 'user')
    search_fields = ('name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'date', 'category', 'type', 'is_paid', 'user')
    list_filter = ('type', 'is_paid', 'date', 'category')
    search_fields = ('description',)
    date_hierarchy = 'date'

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    # Campos que aparecerão na lista do Admin
    list_display = ('category', 'amount', 'month', 'year', 'user')
    # Filtros laterais
    list_filter = ('month', 'year', 'user', 'category')
    # Busca por nome da categoria
    search_fields = ('category__name',)