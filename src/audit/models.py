from django.db import models


class Log(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    http_method = models.CharField(max_length=8)
    path = models.CharField(max_length=255)
    qs = models.TextField(blank=True, null=True)
    remote_ip = models.GenericIPAddressField(null=True)
    user = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        _user = self.user.username if self.user else "Guest"
        _url = f'{self.path}?{self.qs}' if self.qs else self.path
        return f"[{self.timestamp}]: {self.http_method} {_url} | ip: {self.remote_ip}, user: {_user}"
