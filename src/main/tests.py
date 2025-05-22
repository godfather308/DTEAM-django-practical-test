from django.test import Client, TestCase
from django.urls import reverse

from .models import CV, Contact, Project, Skill


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.cv = CV.objects.create(
            first_name="first_name",
            last_name="last_name",
            bio="bio"
        )

        skill = Skill.objects.create(skill="skill")
        project = Project.objects.create(
            project="project",
            description="description",
            start_date="2001-01-01",
            end_date="2025-01-01",
            cv=self.cv
        )
        contact = Contact.objects.create(
            contact="380660001122",
            option="phone",
            cv=self.cv
        )

        self.cv.skills.add(skill)
        self.cv.projects.add(project)
        self.cv.contacts.add(contact)

    def test_cv_list_view(self):
        response = self.client.get(reverse('main:cv_list_view'))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.cv.first_name)
        self.assertContains(response, self.cv.last_name)
        self.assertContains(response, self.cv.bio)
        for skill in self.cv.skills.all():
            self.assertContains(response, skill.skill)
        self.assertTemplateUsed(response, 'main/cv_list_view.html')

    def test_cv_detail_view(self):
        response = self.client.get(reverse('main:cv_detail_view', args=[self.cv.id]))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.cv.first_name)
        self.assertContains(response, self.cv.last_name)
        self.assertContains(response, self.cv.bio)
        for skill in self.cv.skills.all():
            self.assertContains(response, skill.skill)
        for project in self.cv.projects.all():
            self.assertContains(response, project.project)
        for contact in self.cv.contacts.all():
            self.assertContains(response, contact.contact)

        self.assertTemplateUsed(response, 'main/cv_detail_view.html')
