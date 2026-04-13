from django.urls import path
from .views import (
    ResumeListCreateView,
    ResumeDetailView,
    EducationCreateView,
    EducationUpdateDeleteView,
    ExperienceCreateView,
    ExperienceUpdateDeleteView,
    SkillCreateDeleteView,
    ProjectCreateView,
    ProjectUpdateDeleteView,
    CoverLetterListCreateView,
    CoverLetterDetailView,
    ResumeTemplateListView,
    SetResumeTemplateView,
    ResumeVersionListView,
    CreateResumeVersionView,
    RestoreResumeVersionView,
    PublicResumeView,
    GenerateShareLinkView,
    RevokeShareLinkView,
    JobApplicationListCreateView,
    JobApplicationDetailView,
    ResumeAnalyticsView,
    IncrementResumeViewView,
    GeneratePDFView,
    AIEnhanceDescriptionView,
    AIGenerateSummaryView,
)

urlpatterns = [
    # Resume CRUD
    path('', ResumeListCreateView.as_view()),
    path('<int:resume_id>/', ResumeDetailView.as_view()),
    path('<int:resume_id>/template/', SetResumeTemplateView.as_view()),

    # Education
    path('<int:resume_id>/education/', EducationCreateView.as_view()),
    path('education/<int:edu_id>/', EducationUpdateDeleteView.as_view()),

    # Experience
    path('<int:resume_id>/experience/', ExperienceCreateView.as_view()),
    path('experience/<int:exp_id>/', ExperienceUpdateDeleteView.as_view()),

    # Skills
    path('<int:resume_id>/skills/', SkillCreateDeleteView.as_view()),
    path('skills/<int:skill_id>/', SkillCreateDeleteView.as_view()),

    # Projects
    path('<int:resume_id>/projects/', ProjectCreateView.as_view()),
    path('projects/<int:project_id>/', ProjectUpdateDeleteView.as_view()),

    # Cover Letters
    path('<int:resume_id>/cover-letters/', CoverLetterListCreateView.as_view()),
    path('cover-letters/<int:cover_letter_id>/', CoverLetterDetailView.as_view()),

    # Templates
    path('templates/', ResumeTemplateListView.as_view()),

    # Versioning
    path('<int:resume_id>/versions/', ResumeVersionListView.as_view()),
    path('<int:resume_id>/versions/create/', CreateResumeVersionView.as_view()),
    path('<int:resume_id>/versions/<int:version_number>/restore/', RestoreResumeVersionView.as_view()),

    # Public Sharing
    path('public/<uuid:share_code>/', PublicResumeView.as_view()),
    path('<int:resume_id>/share/', GenerateShareLinkView.as_view()),
    path('<int:resume_id>/share/revoke/', RevokeShareLinkView.as_view()),

    # Job Applications
    path('<int:resume_id>/jobs/', JobApplicationListCreateView.as_view()),
    path('jobs/<int:application_id>/', JobApplicationDetailView.as_view()),

    # Analytics
    path('<int:resume_id>/analytics/', ResumeAnalyticsView.as_view()),
    path('<int:resume_id>/analytics/view/', IncrementResumeViewView.as_view()),

    # PDF Generation
    path('<int:resume_id>/pdf/', GeneratePDFView.as_view()),

    # AI Enhancement
    path('<int:resume_id>/ai/enhance/', AIEnhanceDescriptionView.as_view()),
    path('<int:resume_id>/ai/summary/', AIGenerateSummaryView.as_view()),
]
