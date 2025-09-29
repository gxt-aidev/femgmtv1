from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dashboard.views import home_view
from django.conf.urls import handler404
from dashboard import views as dashboard_views
from django.shortcuts import render

def custom_404(request, exception):
    return render(request, "dashboard/404.html", status=404)

handler404 = "field_mgmt.urls.custom_404"

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('', include('accounts.urls', namespace='accounts')),
    path("dashboard/", include(("dashboard.urls", "dashboard"), namespace="dashboard")),
    path('tasks/', include('tasks.urls', namespace='tasks')),
    path('invoices/', include('invoices.urls', namespace='invoices')),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)