import logging

from django.db import transaction

from .models import Log

LOGGER = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        self._log_request(request)
        return response

    @staticmethod
    def _log_request(request):
        if request.path.startswith("/logs/"):
            return

        try:
            with transaction.atomic():
                if not request.path.startswith("/logs/"):
                    Log.objects.create(
                        http_method=request.method,
                        path=request.path,
                        qs=request.META.get('QUERY_STRING', ''),
                        remote_ip=request.META.get('REMOTE_ADDR'),
                        user=request.user if request.user.is_authenticated else None
                    )
        except Exception as e:
            LOGGER.debug(f"RequestLoggingMiddleware error: {e}")
