from django.urls import path
from . import views

app_name = 'invoices'

urlpatterns = [
    path('accounts/invoice/', views.invoice_list, name='invoice_list'),
    path('accounts/invoice/add/', views.invoice_create, name='invoice_add'),
    path('accounts/invoice/<int:pk>/edit/', views.invoice_edit, name='invoice_edit'),
    path('accounts/invoice/<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('accounts/invoice/<int:pk>/pdf/', views.invoice_pdf, name='invoice_pdf'),
    path('accounts/invoice/<int:pk>/send/', views.invoice_send_email, name='invoice_send'),
    path('accounts/invoice/<int:pk>/payment/', views.invoice_add_payment, name='invoice_payment'),
]
