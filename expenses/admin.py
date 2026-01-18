from django.contrib import admin
from .models import Category, Transaction

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