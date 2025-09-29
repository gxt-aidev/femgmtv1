from django import forms
from django.forms import inlineformset_factory
from accounts.models import ClientCompany
from invoices.models import Invoice, InvoiceItem, Payment

class InvoiceForm(forms.ModelForm):
    #     client = forms.ModelChoiceField(
    #     queryset=ClientCompany.objects.filter(active=True),  # filter as needed
    #     label="Client",
    #     empty_label="Select Client"
    # )
        class Meta:
          model = Invoice
          fields = ['client','client_email','client_address','issue_date','due_date','currency','tax_percent','discount','notes','status']

InvoiceItemFormSet = inlineformset_factory(Invoice, InvoiceItem,
                                           fields=('description','quantity','unit_price'),
                                           extra=1, can_delete=True)

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount','paid_at','notes']
