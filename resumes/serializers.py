from rest_framework import serializers
from .models import Resume, Education, Experience, Skill, Project, CoverLetter, ResumeTemplate, ResumeVersion, JobApplication, ResumeAnalytics


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

    def validate(self, data):
        start_year = data.get('start_year')
        end_year = data.get('end_year')

        if start_year and end_year and end_year < start_year:
            raise serializers.ValidationError(
                {"end_year": "End year cannot be before start year"}
            )

        if start_year and (start_year < 1900 or start_year > 2100):
            raise serializers.ValidationError(
                {"start_year": "Start year must be between 1900 and 2100"}
            )

        if end_year and (end_year < 1900 or end_year > 2100):
            raise serializers.ValidationError(
                {"end_year": "End year must be between 1900 and 2100"}
            )

        return data


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

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError(
                {"end_date": "End date cannot be before start date"}
            )

        return data


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


class CoverLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverLetter
        fields = ['id', 'title', 'content', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class ResumeTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeTemplate
        fields = ['id', 'name', 'template_code', 'description', 'is_premium', 'thumbnail_url', 'is_active']


class ResumeVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeVersion
        fields = ['id', 'version_number', 'snapshot_data', 'created_at']
        read_only_fields = ['created_at']


class ResumeSerializer(serializers.ModelSerializer):
    educations = serializers.SerializerMethodField()
    experiences = serializers.SerializerMethodField()
    skills = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()
    template = ResumeTemplateSerializer(read_only=True)
    template_id = serializers.IntegerField(write_only=True, required=False)
    share_code = serializers.UUIDField(read_only=True)

    class Meta:
        model = Resume
        fields = [
            'id',
            'title',
            'created_at',
            'template',
            'template_id',
            'share_code',
            'version',
            'educations',
            'experiences',
            'skills',
            'projects'
        ]

    def get_educations(self, obj):
        return EducationSerializer(obj.educations.filter(is_deleted=False), many=True).data

    def get_experiences(self, obj):
        return ExperienceSerializer(obj.experiences.filter(is_deleted=False), many=True).data

    def get_skills(self, obj):
        return SkillSerializer(obj.skills.filter(is_deleted=False), many=True).data

    def get_projects(self, obj):
        return ProjectSerializer(obj.projects.filter(is_deleted=False), many=True).data

    def create(self, validated_data):
        template_id = validated_data.pop('template_id', None)
        if template_id:
            validated_data['template_id'] = template_id
        return super().create(validated_data)

    def update(self, instance, validated_data):
        template_id = validated_data.pop('template_id', None)
        if template_id:
            instance.template_id = template_id
        return super().update(instance, validated_data)


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = [
            'id',
            'company',
            'position',
            'applied_date',
            'status',
            'job_url',
            'notes',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ResumeAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeAnalytics
        fields = [
            'id',
            'views',
            'downloads',
            'shares',
            'last_viewed_at'
        ]