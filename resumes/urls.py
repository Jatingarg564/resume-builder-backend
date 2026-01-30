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
)

urlpatterns = [
    path('', ResumeListCreateView.as_view()),
    path('<int:resume_id>/', ResumeDetailView.as_view()),

    path('<int:resume_id>/education/', EducationCreateView.as_view()),
    path('education/<int:edu_id>/', EducationUpdateDeleteView.as_view()),

    path('<int:resume_id>/experience/', ExperienceCreateView.as_view()),
    path('experience/<int:exp_id>/', ExperienceUpdateDeleteView.as_view()),

    path('<int:resume_id>/skills/', SkillCreateDeleteView.as_view()),
    path('skills/<int:skill_id>/', SkillCreateDeleteView.as_view()),

    path('<int:resume_id>/projects/', ProjectCreateView.as_view()),
]
