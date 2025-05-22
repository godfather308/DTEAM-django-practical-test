from django.core.exceptions import ValidationError
from django.db import models


class Skill(models.Model):
    skill = models.CharField(max_length=255)

    def __str__(self):
        return self.skill


class CV(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    skills = models.ManyToManyField(Skill)
    bio = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Project(models.Model):
    class Meta:
        ordering = ['-start_date']

    project = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField()
    cv = models.ForeignKey(CV, related_name="projects", on_delete=models.CASCADE)

    def clean(self):
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError("End date cannot be before start date.")

    def __str__(self):
        return self.project


class Contact(models.Model):
    class ContactOption(models.TextChoices):
        EMAIL = 'email'
        PHONE = 'phone'
        GITHUB = 'github'
        LINKEDIN = 'linkedin'
        OTHER = 'other'

    contact = models.CharField(max_length=255)
    option = models.CharField(max_length=255, choices=ContactOption.choices, default=ContactOption.OTHER)
    cv = models.ForeignKey(CV, related_name="contacts", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.option}:<{self.contact}>'
