from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsageViewSet, InvoiceViewSet, dashboard

router = DefaultRouter()
router.register(r'usage', UsageViewSet, basename='usage')
router.register(r'invoice', InvoiceViewSet, basename='invoice')

app_name = 'billing_app'

urlpatterns = [
    # wrap the router.urls in a tuple so include(...) has an app_name
    path('api/', include((router.urls, app_name), namespace='api')),
    path('dashboard/', dashboard, name='dashboard'),
]
