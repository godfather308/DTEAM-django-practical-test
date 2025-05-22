from django.urls import path

from .views import CVDetailView, CVListView, cv_download_pdf, cv_send_email, settings_view

app_name = "main"

urlpatterns = [
    path("", CVListView.as_view(), name="cv_list_view"),
    path("cv/<int:pk>/", CVDetailView.as_view(), name="cv_detail_view"),
    path("cv/<int:pk>/pdf/", cv_download_pdf, name="cv_download_pdf"),
    path("cv/<int:pk>/send/", cv_send_email, name="cv_send_email"),
    path("settings/", settings_view, name="settings"),
]
