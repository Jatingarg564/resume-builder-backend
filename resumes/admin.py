from django.contrib import admin
from .models import (
    Resume, ResumeTemplate, ResumeVersion, Education, Experience,
    Skill, Project, CoverLetter, JobApplication, ResumeAnalytics
)

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at', 'is_deleted']
    list_filter = ['is_deleted', 'created_at']
    search_fields = ['title', 'user__username']

@admin.register(ResumeTemplate)
class ResumeTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'template_code', 'is_premium', 'is_active']
    list_filter = ['is_premium', 'is_active']

@admin.register(ResumeVersion)
class ResumeVersionAdmin(admin.ModelAdmin):
    list_display = ['resume', 'version_number', 'created_at']
    list_filter = ['created_at']

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'institution', 'resume', 'order']
    list_filter = ['is_deleted']

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['role', 'company', 'resume', 'order']
    list_filter = ['is_deleted']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'resume']
    list_filter = ['is_deleted']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'resume', 'order']
    list_filter = ['is_deleted']

@admin.register(CoverLetter)
class CoverLetterAdmin(admin.ModelAdmin):
    list_display = ['title', 'resume', 'created_at']
    list_filter = ['is_deleted']

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['company', 'position', 'status', 'applied_date']
    list_filter = ['status']

@admin.register(ResumeAnalytics)
class ResumeAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['resume', 'views', 'downloads', 'shares']
