from django.urls import path

from .views import RequestLogListView

app_name = "audit"

urlpatterns = [
    path("", RequestLogListView.as_view(), name="logs"),
]
