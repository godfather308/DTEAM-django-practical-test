from django.views.generic import ListView, DetailView
from .models import CV

class CVListView(ListView):
    model = CV
    template_name = 'main/cv_list_view.html'
    context_object_name = 'cvs'

    def get_queryset(self):
        return CV.objects.prefetch_related('skills', 'projects', 'contacts').all()

class CVDetailView(DetailView):
    model = CV
    template_name = 'main/cv_detail_view.html'
    context_object_name = 'cv'

    def get_queryset(self):
        return CV.objects.prefetch_related('skills', 'projects', 'contacts')
