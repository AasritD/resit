# services/core_project/app/user_management/urls.py

from django.urls import path
from .views import (
    login_view,
    logout_view,
    dashboard_redirect_view,
    register_view,  # new import
)

app_name = 'user_management'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_redirect_view, name='dashboard'),
    path('register/', register_view, name='register'),  # new route
]
