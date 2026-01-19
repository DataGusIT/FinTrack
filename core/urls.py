from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), # URLs padrão de login/logout
    path('', include('dashboard.urls')),
    # path('expenses/', include('expenses.urls')), # Criar depois
]