from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    # Transações (mantenha as existentes)
    path('novo/', views.transaction_create, name='create'),
    path('editar/<int:pk>/', views.transaction_update, name='update'),
    path('deletar/<int:pk>/', views.transaction_delete, name='delete'),
    
    # Categorias (novas rotas)
    path('categorias/', views.category_list, name='category_list'),
    path('categorias/novo/', views.category_create, name='category_create'),
    path('categorias/editar/<int:pk>/', views.category_update, name='category_update'),
    path('categorias/deletar/<int:pk>/', views.category_delete, name='category_delete'),
]