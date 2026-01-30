from rest_framework import serializers
from .models import Resume, Education, Experience, Skill, Project

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = [
            'id',
            'degree',
            'institution',
            'start_year',
            'end_year'
        ]
        
class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = [
            'id',
            'company',
            'role',
            'start_date',
            'end_date',
            'description'
        ]
        
class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']
        
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'description',
            'tech_stack',
            'project_link'
        ]

class ResumeSerializer(serializers.ModelSerializer):
    educations = EducationSerializer(many=True, read_only=True)
    experiences = ExperienceSerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Resume
        fields = [
            'id',
            'title',
            'created_at',
            'educations',
            'experiences',
            'skills',
            'projects'
        ]
