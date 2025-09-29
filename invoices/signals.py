from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Invoice
from django.utils import timezone

@receiver(pre_save, sender=Invoice)
def set_invoice_number(sender, instance, **kwargs):
    if not instance.number:
        # format: INV-YYYYMM-0001
        today = timezone.now().date()
        prefix = f"INV-{today.strftime('%Y%m')}-"
        # find max existing number for month
        last = Invoice.objects.filter(number__startswith=prefix).order_by('-number').first()
        if last and last.number.startswith(prefix):
            last_seq = int(last.number.replace(prefix, ''))
            new_seq = last_seq + 1
        else:
            new_seq = 1
        instance.number = f"{prefix}{new_seq:04d}"
