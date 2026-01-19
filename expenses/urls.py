from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('novo/', views.transaction_create, name='create'),
    path('editar/<int:pk>/', views.transaction_update, name='update'),
    path('deletar/<int:pk>/', views.transaction_delete, name='delete'),
]