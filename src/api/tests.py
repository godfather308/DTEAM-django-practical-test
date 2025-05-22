from django.urls import reverse
from main.models import Contact, CV, Project, Skill

from rest_framework.test import APITestCase
from rest_framework import status


class APIViewsTest(APITestCase):
    def setUp(self):
        skills_data = [
            {"skill": "Django"},
            {"skill": "Flask"},
            {"skill": "FastAPI"},
            {"skill": "Celery"},
            {"skill": "Docker"},
        ]
        skills = [Skill.objects.create(**skill_data) for skill_data in skills_data]

        self.cv_data = {
            "first_name": "Rey",
            "last_name": "Mysterio",
            "bio": "619 Wrestler",
        }
        self.cv = CV.objects.create(**self.cv_data)
        self.cv.skills.set(skills)

        project_data = {
            "project": "WWE",
            "description": "Wrestling project",
            "start_date": "2004-01-01",
            "end_date": "2018-01-01",
        }
        Project.objects.create(cv=self.cv, **project_data)

        contact_data = {"option": "phone", "contact": "rey_mysterio@wwe.com"}
        Contact.objects.create(cv=self.cv, **contact_data)

    def test_create_cv(self):
        cv_data = {
            "first_name": "Big",
            "last_name": "Show",
            "bio": "Skilled developer",
            "projects": [{
                "project": "WWE",
                "description": "Big wrestling project",
                "start_date": "2000-01-01",
                "end_date": "2020-01-01",
            }],
            "skills": [{"skill": "BigQueries"},{"skill": "SoBigQueries"}],
            "contacts": [{"option": "phone", "contact": "big_show@wwe.com"},],
        }
        url = reverse('api:cvs-list')
        response = self.client.post(url, cv_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(CV.objects.count(), 2)
        self.assertEqual(Project.objects.count(), 2)
        self.assertEqual(Skill.objects.count(), 7)
        self.assertEqual(Contact.objects.count(), 2)

    def test_get_cv_list(self):
        url = reverse('api:cvs-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_cv_detail(self):
        url = reverse('api:cvs-detail', kwargs={'pk': self.cv.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Rey')
        self.assertEqual(len(response.data['skills']), 5)
        self.assertEqual(len(response.data['projects']), 1)
        self.assertEqual(len(response.data['contacts']), 1)


    def test_update_cv(self):
        url = reverse('api:cvs-detail', kwargs={'pk': self.cv.pk})
        patch_data = {
            "bio": "619 Wrestler & Luchador"
        }

        response = self.client.patch(url, patch_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cv.refresh_from_db()
        self.assertEqual(self.cv.bio, '619 Wrestler & Luchador')
        self.assertEqual(self.cv.first_name, 'Rey')
        self.assertEqual(self.cv.last_name, 'Mysterio')

    def test_delete_cv(self):
        url = reverse('api:cvs-detail', kwargs={'pk': self.cv.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CV.objects.count(), 0)
        self.assertEqual(Project.objects.count(), 0)
        self.assertEqual(Contact.objects.count(), 0)
