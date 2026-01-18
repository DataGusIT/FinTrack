from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Define quais campos aparecerão no formulário de edição do Admin
    fieldsets = UserAdmin.fieldsets + (
        ('Preferências Financeiras', {'fields': ('preferred_currency',)}),
    )
    # Define quais campos aparecerão no formulário de criação
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Preferências Financeiras', {'fields': ('preferred_currency',)}),
    )