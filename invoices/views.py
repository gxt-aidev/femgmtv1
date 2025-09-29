from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse
from .models import Invoice
from .forms import InvoiceForm, InvoiceItemFormSet, PaymentForm
from decimal import Decimal
from django.template.loader import render_to_string
import weasyprint
from django.conf import settings
from django.core.mail import EmailMessage

def is_accounts(user):
    return user.is_authenticated and getattr(user, "role", None) in ['accounts','admin','manager']

@login_required
@user_passes_test(is_accounts)
def invoice_list(request):
    qs = Invoice.objects.all()
    return render(request, 'invoices/invoice_list.html', {'invoices': qs})

@login_required
@user_passes_test(is_accounts)
def invoice_create(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        formset = InvoiceItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            invoice = form.save(commit=False)
            invoice.created_by = request.user
            invoice.save()
            formset.instance = invoice
            formset.save()
            messages.success(request, "Invoice created.")
            return redirect('invoices:invoice_detail', invoice.pk)
    else:
        form = InvoiceForm()
        formset = InvoiceItemFormSet()
    return render(request, 'invoices/invoice_form.html', {'form': form, 'formset': formset})

@login_required
@user_passes_test(is_accounts)
def invoice_edit(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if invoice.status == 'paid':
        messages.error(request, "Paid invoices cannot be edited.")
        return redirect(invoice.get_absolute_url())
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        formset = InvoiceItemFormSet(request.POST, instance=invoice)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Invoice updated.")
            return redirect(invoice.get_absolute_url())
    else:
        form = InvoiceForm(instance=invoice)
        formset = InvoiceItemFormSet(instance=invoice)
    return render(request, 'invoices/invoice_form.html', {'form': form, 'formset': formset, 'invoice': invoice})

@login_required
@user_passes_test(is_accounts)
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    payment_form = PaymentForm()
    return render(request, 'invoices/invoice_detail.html', {'invoice': invoice, 'payment_form': payment_form})

@login_required
@user_passes_test(is_accounts)
def invoice_add_payment(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            p.invoice = invoice
            p.created_by = request.user
            p.save()
            # update invoice status
            if invoice.balance_due() <= Decimal('0.00'):
                invoice.status = 'paid'
            elif invoice.paid_amount() > Decimal('0.00'):
                invoice.status = 'partial'
            invoice.save()
            messages.success(request, "Payment recorded.")
    return redirect(invoice.get_absolute_url())

@login_required
@user_passes_test(is_accounts)
def invoice_pdf(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    html = render_to_string('invoices/invoice_pdf.html', {'invoice': invoice})
    # create pdf with weasyprint
    pdf = weasyprint.HTML(string=html, base_url=request.build_absolute_uri('/')).write_pdf(stylesheets=[weasyprint.CSS(string='@page { size: A4; margin: 20mm }')])
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{invoice.number}.pdf"'
    return response

@login_required
@user_passes_test(is_accounts)
def invoice_send_email(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    # render PDF bytes
    html = render_to_string('invoices/invoice_pdf.html', {'invoice': invoice})
    pdf = weasyprint.HTML(string=html, base_url=request.build_absolute_uri('/')).write_pdf()
    subject = f"Invoice {invoice.number} from YourCompany"
    body = "Please find attached the invoice."
    email = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [invoice.client_email])
    email.attach(f"{invoice.number}.pdf", pdf, 'application/pdf')
    email.send(fail_silently=False)
    invoice.status = 'sent'
    invoice.save()
    messages.success(request, "Invoice emailed to client.")
    return redirect(invoice.get_absolute_url())
