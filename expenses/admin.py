from django.contrib import admin
from .models import Category, Transaction, Budget

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'user')
    list_filter = ('type', 'user')
    search_fields = ('name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    # REMOVEMOS 'is_paid' e ADICIONAMOS 'status' e 'payment_method'
    list_display = ('description', 'amount', 'date', 'category', 'type', 'status', 'payment_method', 'user')
    
    # Atualizamos os filtros laterais também
    list_filter = ('type', 'status', 'payment_method', 'date', 'category')
    
    search_fields = ('description',)
    date_hierarchy = 'date'

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('category', 'amount', 'month', 'year', 'user')
    list_filter = ('month', 'year', 'user', 'category')
    search_fields = ('category__name',)