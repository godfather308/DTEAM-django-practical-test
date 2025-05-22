from django.views.generic import ListView

from .models import Log


class RequestLogListView(ListView):
    model = Log
    template_name = 'audit/logs_list_view.html'
    context_object_name = 'logs'

    def get_queryset(self):
        return Log.objects.select_related('user')[:10]
