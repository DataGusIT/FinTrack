from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('novo/', views.transaction_create, name='create'),
]