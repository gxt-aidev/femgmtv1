from decimal import Decimal, ROUND_HALF_UP
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from accounts.models import ClientCompany

User = settings.AUTH_USER_MODEL

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('partial', 'Partially Paid'),
        ('cancelled', 'Cancelled'),
    ]

    number = models.CharField(max_length=32, unique=True, blank=True)
    client = models.ForeignKey(ClientCompany, null=True, blank=True,related_name="invoices",on_delete=models.CASCADE)
    client_email = models.EmailField(blank=True, null=True)
    client_address = models.TextField(blank=True)
    issue_date = models.DateField(default=timezone.localdate)
    due_date = models.DateField(null=True, blank=True)
    currency = models.CharField(max_length=8, default='INR')   # adapt
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='invoices_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-issue_date', '-created_at']

    def __str__(self):
        return f"{self.number or 'UNSET'} — {self.client_name}"

    def subtotal(self):
        return sum([item.line_total() for item in self.items.all()])

    def tax_amount(self):
        return (self.subtotal() * (self.tax_percent or Decimal('0.00')) / Decimal('100')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def total(self):
        total = self.subtotal() + self.tax_amount() - (self.discount or Decimal('0.00'))
        return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def paid_amount(self):
        return sum([p.amount for p in self.payments.all()]) or Decimal('0.00')

    def balance_due(self):
        return (self.total() - self.paid_amount()).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def get_absolute_url(self):
        return reverse('invoices:invoice_detail', args=[self.pk])

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    description = models.CharField(max_length=512)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        ordering = ['id']

    def line_total(self):
        return (self.quantity * self.unit_price).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_at = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-paid_at']
