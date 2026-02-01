from django.contrib import admin
from django.urls import path
from finance import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.dashboard, name="dashboard"),
    path("export/csv/", views.export_csv, name="export_csv"),
]
