from rest_framework import serializers

from main.models import CV, Contact, Project, Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'skill']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'project', 'description', 'start_date', 'end_date']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'contact', 'option']


class CVSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, required=False)
    projects = ProjectSerializer(many=True, required=False)
    contacts = ContactSerializer(many=True, required=False)

    class Meta:
        model = CV
        fields = ['id', 'first_name', 'last_name', 'bio', 'skills', 'projects', 'contacts']

    def create(self, validated_data):
        skills_data = validated_data.pop('skills', [])
        projects_data = validated_data.pop('projects', [])
        contacts_data = validated_data.pop('contacts', [])

        cv = CV.objects.create(**validated_data)

        for skill_data in skills_data:
            skill_obj, _ = Skill.objects.get_or_create(**skill_data)
            cv.skills.add(skill_obj)

        for project_data in projects_data:
            Project.objects.create(cv=cv, **project_data)

        for contact_data in contacts_data:
            Contact.objects.create(cv=cv, **contact_data)

        return cv
