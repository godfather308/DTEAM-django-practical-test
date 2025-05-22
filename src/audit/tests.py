from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Log


class RequestLoggingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test_user',
            password='1user_test2'
        )

    def test_request_logging_basic(self):
        self.client.get(reverse('main:cv_list_view'))
        self.client.get(reverse('api:cvs-list'))

        self.assertEqual(Log.objects.count(), 2)

        log_cv_list = Log.objects.get(pk=1)
        self.assertEqual(log_cv_list.http_method, 'GET')
        self.assertEqual(log_cv_list.path, '/')

        log_api_cv_list = Log.objects.get(pk=2)
        self.assertEqual(log_api_cv_list.http_method, 'GET')
        self.assertEqual(log_api_cv_list.path, '/api/cvs/')

    def test_show_10(self):
        test_log_amount = 11
        for _ in range(test_log_amount):
            Log.objects.create(
                http_method='GET',
                path=f'/',
                remote_ip='127.0.0.1'
            )

        response = self.client.get(reverse('audit:logs'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['logs']), 10)

    def test_logs_sort(self):
        test_log_amount = 11
        logs = [Log.objects.create(
            http_method='GET',
            path=f'/',
            remote_ip='127.0.0.1'
        ) for _ in range(test_log_amount)]

        response = self.client.get(reverse('audit:logs'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['logs'][0].timestamp, logs[-1].timestamp)
