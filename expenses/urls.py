from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    # Transações
    path('novo/', views.transaction_create, name='create'),
    path('editar/<int:pk>/', views.transaction_update, name='update'),
    path('deletar/<int:pk>/', views.transaction_delete, name='delete'),
    path('extrato/', views.transaction_list, name='transaction_list'),
    path('pagar/<int:pk>/', views.transaction_pay, name='pay'),

    # Categorias 
    path('categorias/', views.category_list, name='category_list'),
    path('categorias/novo/', views.category_create, name='category_create'),
    path('categorias/editar/<int:pk>/', views.category_update, name='category_update'),
    path('categorias/deletar/<int:pk>/', views.category_delete, name='category_delete'),

    # Orçamentos
    path('orcamentos/', views.budget_list, name='budget_list'),
    path('orcamentos/novo/', views.budget_create, name='budget_create'),
    path('orcamentos/editar/<int:pk>/', views.budget_update, name='budget_update'),
    path('orcamentos/deletar/<int:pk>/', views.budget_delete, name='budget_delete'),

    # Recorrencias 
    path('recorrentes/', views.recurring_list, name='recurring_list'),
    path('recorrentes/novo/', views.recurring_create, name='recurring_create'),
    path('recorrentes/editar/<int:pk>/', views.recurring_update, name='recurring_update'),
    path('recorrentes/deletar/<int:pk>/', views.recurring_delete, name='recurring_delete'),

    path('exportar/csv/', views.export_transactions_csv, name='export_csv'),
]