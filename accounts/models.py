from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Aqui podemos adicionar campos extras no futuro
    # Por enquanto, apenas herdamos o padrão para garantir a flexibilidade
    email = models.EmailField('E-mail', unique=True)
    
    # Exemplo de campo extra para um sistema financeiro
    CURRENCY_CHOICES = (
        ('BRL', 'Real Brasileiro'),
        ('USD', 'Dólar Americano'),
        ('EUR', 'Euro'),
    )
    preferred_currency = models.CharField(
        max_length=3, 
        choices=CURRENCY_CHOICES, 
        default='BRL'
    )

    def __str__(self):
        return self.username