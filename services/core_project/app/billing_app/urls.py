# services/core_project/app/billing_app/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsageViewSet, InvoiceViewSet, dashboard, InvoicePDFView

router = DefaultRouter()
router.register(r'usage', UsageViewSet, basename='usage')
router.register(r'invoice', InvoiceViewSet, basename='invoice')

app_name = 'billing_app'  # ← IMPORTANT: match this in models.py reverse() and other references

urlpatterns = [
    # REST API endpoints under /api/
    path('api/', include((router.urls, app_name), namespace='api')),

    # HTML dashboard
    path('dashboard/', dashboard, name='dashboard'),

    # PDF download endpoint, used by Invoice.get_pdf_url()
    path('invoice/<int:pk>/pdf/', InvoicePDFView.as_view(), name='invoice-pdf'),
]
