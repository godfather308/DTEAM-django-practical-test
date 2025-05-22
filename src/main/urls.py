from django.urls import path
from .views import CVListView, CVDetailView, cv_download_pdf

app_name = "main"

urlpatterns = [
    path("", CVListView.as_view(), name="cv_list_view"),
    path("cv/<int:pk>/", CVDetailView.as_view(), name="cv_detail_view"),
    path("cv/<int:pk>/pdf/", cv_download_pdf, name="cv_download_pdf"),
]
