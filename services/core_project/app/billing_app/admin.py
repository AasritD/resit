from django.contrib import admin
from django.utils.html import format_html
from .models import UsageRecord, Invoice

@admin.register(UsageRecord)
class UsageRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'endpoint', 'timestamp')
    list_filter = ('endpoint', 'user')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('user', 'period_start', 'period_end', 'total_calls', 'amount_due', 'generated_at', 'download_link')

    def download_link(self, obj):
        return format_html('<a href="{}">PDF</a>', obj.get_pdf_url())
    download_link.short_description = "Invoice PDF"
