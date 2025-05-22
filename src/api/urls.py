from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CVViewSet

router = DefaultRouter()
router.register(r'cvs', CVViewSet, basename='cvs')

app_name = "main_api"

urlpatterns = router.urls
