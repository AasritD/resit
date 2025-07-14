# services/core_project/app/uploads/urls.py

from django.urls import path
from .views import dashboard

app_name = 'uploads'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
]
