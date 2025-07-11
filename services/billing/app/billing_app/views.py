from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import UsageRecord, Invoice
from .serializers import UsageRecordSerializer, InvoiceSerializer
from reportlab.pdfgen import canvas
from io import BytesIO


class UsageViewSet(viewsets.ModelViewSet):
    queryset = UsageRecord.objects.all().order_by('-timestamp')
    serializer_class = UsageRecordSerializer

class InvoiceViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def generate(self, request):
        user = request.user
        start = request.data.get('start')
        end = request.data.get('end')
        qs = UsageRecord.objects.filter(user=user,
            timestamp__date__gte=start, timestamp__date__lte=end)
        total = qs.count()
        amount = total * 0.10  # e.g. $0.10 per call
        inv = Invoice.objects.create(user=user,
            period_start=start, period_end=end,
            total_calls=total, amount_due=amount)
        # create PDF
        buffer=BytesIO()
        p=canvas.Canvas(buffer)
        p.drawString(100,800,f"Invoice for {user.username}")
        p.drawString(100,780,f"Period: {start} to {end}")
        p.drawString(100,760,f"Calls: {total}")
        p.drawString(100,740,f"Amount due: ${amount:.2f}")
        p.showPage(); p.save()
        buffer.seek(0)
        inv_pdf=buffer.read()
        return Response({'invoice_id':inv.id,'pdf':inv_pdf},status=status.HTTP_201_CREATED)

@login_required
def dashboard(request):
    """
    Simple billing dashboard view.
    URL: /billing/dashboard/
    """
    return render(request, 'billing/dashboard.html')