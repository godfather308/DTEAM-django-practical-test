from django.urls import path

from .views import CVDetailView, CVListView, cv_download_pdf, settings_view

app_name = "main"

urlpatterns = [
    path("", CVListView.as_view(), name="cv_list_view"),
    path("cv/<int:pk>/", CVDetailView.as_view(), name="cv_detail_view"),
    path("cv/<int:pk>/pdf/", cv_download_pdf, name="cv_download_pdf"),
    path("settings/", settings_view, name="settings"),
]
