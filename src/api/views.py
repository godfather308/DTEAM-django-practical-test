from rest_framework.viewsets import ModelViewSet

from main.models import CV
from .serializers import CVSerializer


class CVViewSet(ModelViewSet):
    queryset = CV.objects.prefetch_related('skills', 'projects', 'contacts')
    serializer_class = CVSerializer
