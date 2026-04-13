from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .models import Resume, Education, Experience, Skill, Project, CoverLetter, ResumeTemplate, ResumeVersion, JobApplication, ResumeAnalytics
from .serializers import (
    ResumeSerializer, EducationSerializer, ExperienceSerializer,
    SkillSerializer, ProjectSerializer, CoverLetterSerializer,
    ResumeTemplateSerializer, ResumeVersionSerializer,
    JobApplicationSerializer, ResumeAnalyticsSerializer
)
import json
import uuid
from django.utils import timezone
import os


# PDF Generation Service
class PDFGenerator:
    @staticmethod
    def generate_html(resume):
        """Generate HTML content for resume PDF"""
        educations = resume.educations.filter(is_deleted=False)
        experiences = resume.experiences.filter(is_deleted=False)
        skills = resume.skills.filter(is_deleted=False)
        projects = resume.projects.filter(is_deleted=False)

        template_code = resume.template.template_code if resume.template else 'classic'

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1 {{ color: #333; border-bottom: 2px solid #333; padding-bottom: 10px; }}
                h2 {{ color: #666; margin-top: 20px; }}
                .section {{ margin-bottom: 20px; }}
                .item {{ margin-bottom: 10px; }}
                .date {{ color: #666; font-size: 0.9em; }}
                .skills {{ display: flex; flex-wrap: wrap; gap: 10px; }}
                .skill-tag {{ background: #eee; padding: 3px 10px; border-radius: 3px; }}
            </style>
        </head>
        <body>
            <h1>{resume.title}</h1>

            <div class="section">
                <h2>Education</h2>
                {''.join([f'''
                <div class="item">
                    <strong>{edu.degree}</strong> - {edu.institution}
                    <div class="date">{edu.start_year} - {edu.end_year or 'Present'}</div>
                </div>
                ''' for edu in educations])}
            </div>

            <div class="section">
                <h2>Experience</h2>
                {''.join([f'''
                <div class="item">
                    <strong>{exp.role}</strong> at {exp.company}
                    <div class="date">{exp.start_date} - {exp.end_date or 'Present'}</div>
                    <p>{exp.description}</p>
                </div>
                ''' for exp in experiences])}
            </div>

            <div class="section">
                <h2>Skills</h2>
                <div class="skills">
                    {''.join([f'<span class="skill-tag">{skill.name}</span>' for skill in skills])}
                </div>
            </div>

            <div class="section">
                <h2>Projects</h2>
                {''.join([f'''
                <div class="item">
                    <strong>{proj.title}</strong>
                    <p>{proj.description}</p>
                    <div class="date">Tech: {proj.tech_stack}</div>
                </div>
                ''' for proj in projects])}
            </div>
        </body>
        </html>
        """
        return html


# AI Enhancement Service
class AIEnhancer:
    @staticmethod
    def enhance_description(description):
        """Enhance bullet points using OpenAI"""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a resume writing expert. Improve the following bullet points to be more impactful and professional. Keep it concise."},
                    {"role": "user", "content": description}
                ],
                max_tokens=500
            )

            return response.choices[0].message.content
        except Exception as e:
            return f"AI enhancement failed: {str(e)}"

    @staticmethod
    def generate_summary(resume):
        """Generate professional summary using OpenAI"""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

            # Collect resume data
            skills = [s.name for s in resume.skills.filter(is_deleted=False)]
            experiences = resume.experiences.filter(is_deleted=False)[:2]

            prompt = f"""
            Generate a professional summary for a resume based on:
            - Skills: {', '.join(skills)}
            - Latest experiences: {', '.join([f'{e.role} at {e.company}' for e in experiences])}

            Keep it concise (2-3 sentences).
            """

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a resume writing expert. Generate professional summaries."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200
            )

            return response.choices[0].message.content
        except Exception as e:
            return f"AI enhancement failed: {str(e)}"


# Job Application Views
class JobApplicationListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, resume_id):
        resume = Resume.objects.filter(
            id=resume_id,
            user=request.user,
            is_deleted=False
        ).first()

        if not resume:
            return Response(
                {"error": "Resume not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        applications = JobApplication.objects.filter(resume=resume)
        serializer = JobApplicationSerializer(applications, many=True)
        return Response(serializer.data)

    def post(self, request, resume_id):
        resume = Resume.objects.filter(
            id=resume_id,
            user=request.user,
            is_deleted=False
        ).first()

        if not resume:
            return Response(
                {"error": "Resume not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = JobApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(resume=resume)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobApplicationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, application_id):
        application = JobApplication.objects.filter(
            id=application_id,
            resume__user=request.user
        ).first()

        if not application:
            return Response(
                {"error": "Job application not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = JobApplicationSerializer(application)
        return Response(serializer.data)

    def patch(self, request, application_id):
        application = JobApplication.objects.filter(
            id=application_id,
            resume__user=request.user
        ).first()

        if not application:
            return Response(
                {"error": "Job application not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = JobApplicationSerializer(application, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, application_id):
        application = JobApplication.objects.filter(
            id=application_id,
            resume__user=request.user
        ).first()

        if not application:
            return Response(
                {"error": "Job application not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        application.delete()
        return Response(
            {"message": "Job application deleted"},
            status=status.HTTP_204_NO_CONTENT
        )


# Resume Analytics Views
class ResumeAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, resume_id):
        resume = Resume.objects.filter(
            id=resume_id,
            user=request.user,
            is_deleted=False
        ).first()

        if not resume:
            return Response(
                {"error": "Resume not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        analytics, created = ResumeAnalytics.objects.get_or_create(resume=resume)
        serializer = ResumeAnalyticsSerializer(analytics)
        return Response(serializer.data)


class IncrementResumeViewView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, resume_id):
        # For public views, no auth required
        resume = Resume.objects.filter(
            id=resume_id,
            is_deleted=False
        ).first()

        if not resume:
            return Response(
                {"error": "Resume not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        analytics, created = ResumeAnalytics.objects.get_or_create(resume=resume)
        analytics.views += 1
        analytics.last_viewed_at = timezone.now()
        analytics.save()

        return Response({"views": analytics.views})


# PDF Generation Views
class GeneratePDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, resume_id):
        resume = Resume.objects.filter(
            id=resume_id,
            user=request.user,
            is_deleted=False
        ).first()

        if not resume:
            return Response(
                {"error": "Resume not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        html_content = PDFGenerator.generate_html(resume)

        # Track download
        analytics, created = ResumeAnalytics.objects.get_or_create(resume=resume)
        analytics.downloads += 1
        analytics.save()

        return Response({
            "html": html_content,
            "message": "PDF generated. Use a PDF library to convert HTML to PDF."
        })


# AI Enhancement Views
class AIEnhanceDescriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, resume_id):
        resume = Resume.objects.filter(
            id=resume_id,
            user=request.user,
            is_deleted=False
        ).first()

        if not resume:
            return Response(
                {"error": "Resume not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        description = request.data.get('description')
        if not description:
            return Response(
                {"error": "description is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        enhanced = AIEnhancer.enhance_description(description)
        return Response({"enhanced": enhanced})


class AIGenerateSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, resume_id):
        resume = Resume.objects.filter(
            id=resume_id,
            user=request.user,
            is_deleted=False
        ).first()

        if not resume:
            return Response(
                {"error": "Resume not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        summary = AIEnhancer.generate_summary(resume)
        return Response({"summary": summary})


class ResumeListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        resumes = Resume.objects.filter(user=request.user, is_deleted=False)

        # Add search functionality
        search_query = request.query_params.get('search', None)
        if search_query:
            resumes = resumes.filter(title__icontains=search_query)

        serializer = ResumeSerializer(resumes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ResumeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EducationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, resume_id):
        try:
            resume = Resume.objects.get(
                id=resume_id,
                user=request.user,
                is_deleted=False
            )
        except Resume.DoesNotExist:
            return Response(
                {"error": "Resume not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = EducationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(resume=resume)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EducationUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, edu_id):
        try:
            education = Education.objects.get(
                id=edu_id,
                resume__user=request.user,
                resume__is_deleted=False,
                is_deleted=False
            )
        except Education.DoesNotExist:
            return Response(
                {"error": "Education not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = EducationSerializer(
            education,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, edu_id):
        try:
            education = Education.objects.get(
                id=edu_id,
                resume__user=request.user,
                resume__is_deleted=False
            )
        except Education.DoesNotExist:
            return Response(
                {"error": "Education not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        education.is_deleted = True
        education.save()
        return Response(
            {"message": "Education deleted"},
            status=status.HTTP_204_NO_CONTENT
        )
    
class ExperienceCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, resume_id):
        try:
            resume = Resume.objects.get(
                id=resume_id,
                user=request.user,
                is_deleted=False
            )
        except Resume.DoesNotExist:
            return Response(
                {"error": "Resume not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ExperienceSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(resume=resume)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExperienceUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, exp_id):
        try:
            experience = Experience.objects.get(
                id=exp_id,
                resume__user=request.user,
                resume__is_deleted=False,
                is_deleted=False
            )
        except Experience.DoesNotExist:
            return Response(
                {"error": "Experience not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ExperienceSerializer(
            experience,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, exp_id):
        try:
            experience = Experience.objects.get(
                id=exp_id,
                resume__user=request.user,
                resume__is_deleted=False
            )
        except Experience.DoesNotExist:
            return Response(
                {"error": "Experience not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        experience.is_deleted = True
        experience.save()
        return Response(
            {"message": "Experience deleted"},
            status=status.HTTP_204_NO_CONTENT
        )

class SkillCreateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, resume_id):
        resume = Resume.objects.filter(
            id=resume_id,
            user=request.user,
            is_deleted=False
        ).first()

        if not resume:
            return Response(
                {"error": "Resume not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = SkillSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(resume=resume)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, skill_id):
        skill = Skill.objects.filter(
            id=skill_id,
            resume__user=request.user,
            resume__is_deleted=False
        ).first()

        if not skill:
            return Response(
                {"error": "Skill not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        skill.is_deleted = True
        skill.save()
        return Response(
            {"message": "Skill deleted"},
            status=status.HTTP_204_NO_CONTENT
        )
        
class ProjectCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, resume_id):
        resume = Resume.objects.filter(
            id=resume_id,
            user=request.user,
            is_deleted=False
        ).first()

        if not resume:
            return Response(
                {"error": "Resume not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProjectSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(resume=resume)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        project = Project.objects.filter(
            id=project_id,
            resume__user=request.user,
            resume__is_deleted=False,
            is_deleted=False
        ).first()

        if not project:
            return Response(
                {"error": "Project not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def patch(self, request, project_id):
        project = Project.objects.filter(
            id=project_id,
            resume__user=request.user,
            resume__is_deleted=False
        ).first()

        if not project:
            return Response(
                {"error": "Project not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProjectSerializer(project, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id):
        project = Project.objects.filter(
            id=project_id,
            resume__user=request.user,
            resume__is_deleted=False
        ).first()

        if not project:
            return Response(
                {"error": "Project not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        project.is_deleted = True
        project.save()
        return Response(
            {"message": "Project deleted"},
            status=status.HTTP_204_NO_CONTENT
        )


class ResumeDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, resume_id):
        try:
            resume = Resume.objects.get(
                id=resume_id,
                user=request.user,
                is_deleted=False
            )
        except Resume.DoesNotExist:
            return Response(
                {"error": "Resume not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ResumeSerializer(resume)
        return Response(serializer.data)

    def patch(self, request, resume_id):
        try:
            resume = Resume.objects.get(
                id=resume_id,
                user=request.user,
                is_deleted=False
            )
        except Resume.DoesNotExist:
            return Response(
                {"error": "Resume not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ResumeSerializer(resume, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, resume_id):
        try:
            resume = Resume.objects.get(
                id=resume_id,
                user=request.user,
                is_deleted=False
            )
        except Resume.DoesNotExist:
            return Response(
                {"error": "Resume not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        resume.is_deleted = True
        resume.save()
        return Response(
            {"message": "Resume deleted"},
            status=status.HTTP_204_NO_CONTENT
        )


# Cover Letter Views
class CoverLetterListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, resume_id):
        resume = Resume.objects.filter(
            id=resume_id,
            user=request.user,
            is_deleted=False
        ).first()

        if not resume:
            return Response(
                {"error": "Resume not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        cover_letters = CoverLetter.objects.filter(resume=resume, is_deleted=False)
        serializer = CoverLetterSerializer(cover_letters, many=True)
        return Response(serializer.data)

    def post(self, request, resume_id):
        resume = Resume.objects.filter(
            id=resume_id,
            user=request.user,
            is_deleted=False
        ).first()

        if not resume:
            return Response(
                {"error": "Resume not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CoverLetterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(resume=resume)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CoverLetterDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, cover_letter_id):
        cover_letter = CoverLetter.objects.filter(
            id=cover_letter_id,
            resume__user=request.user,
            resume__is_deleted=False,
            is_deleted=False
        ).first()

        if not cover_letter:
            return Response(
                {"error": "Cover letter not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CoverLetterSerializer(cover_letter)
        return Response(serializer.data)

    def patch(self, request, cover_letter_id):
        cover_letter = CoverLetter.objects.filter(
            id=cover_letter_id,
            resume__user=request.user,
            resume__is_deleted=False
        ).first()

        if not cover_letter:
            return Response(
                {"error": "Cover letter not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CoverLetterSerializer(cover_letter, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, cover_letter_id):
        cover_letter = CoverLetter.objects.filter(
            id=cover_letter_id,
            resume__user=request.user,
            resume__is_deleted=False
        ).first()

        if not cover_letter:
            return Response(
                {"error": "Cover letter not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        cover_letter.is_deleted = True
        cover_letter.save()
        return Response(
            {"message": "Cover letter deleted"},
            status=status.HTTP_204_NO_CONTENT
        )


# Resume Template Views
class ResumeTemplateListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        templates = ResumeTemplate.objects.filter(is_active=True)
        serializer = ResumeTemplateSerializer(templates, many=True)
        return Response(serializer.data)


class SetResumeTemplateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, resume_id):
        resume = Resume.objects.filter(
            id=resume_id,
            user=request.user,
            is_deleted=False
        ).first()

        if not resume:
            return Response(
                {"error": "Resume not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        template_id = request.data.get('template_id')
        if not template_id:
            return Response(
                {"error": "template_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        template = ResumeTemplate.objects.filter(id=template_id, is_active=True).first()
        if not template:
            return Response(
                {"error": "Template not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        resume.template = template
        resume.save()

        serializer = ResumeSerializer(resume)
        return Response(serializer.data)


# Resume Versioning Views
class ResumeVersionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, resume_id):
        resume = Resume.objects.filter(
            id=resume_id,
            user=request.user,
            is_deleted=False
        ).first()

        if not resume:
            return Response(
                {"error": "Resume not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        versions = ResumeVersion.objects.filter(resume=resume)
        serializer = ResumeVersionSerializer(versions, many=True)
        return Response(serializer.data)


class CreateResumeVersionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, resume_id):
        resume = Resume.objects.filter(
            id=resume_id,
            user=request.user,
            is_deleted=False
        ).first()

        if not resume:
            return Response(
                {"error": "Resume not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Create snapshot of current resume data
        snapshot = {
            'title': resume.title,
            'educations': list(resume.educations.filter(is_deleted=False).values()),
            'experiences': list(resume.experiences.filter(is_deleted=False).values()),
            'skills': list(resume.skills.filter(is_deleted=False).values()),
            'projects': list(resume.projects.filter(is_deleted=False).values()),
        }

        # Increment version
        new_version = resume.version + 1
        resume.version = new_version
        resume.save()

        # Create version record
        ResumeVersion.objects.create(
            resume=resume,
            version_number=new_version,
            snapshot_data=snapshot
        )

        serializer = ResumeSerializer(resume)
        return Response(serializer.data)


class RestoreResumeVersionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, resume_id, version_number):
        resume = Resume.objects.filter(
            id=resume_id,
            user=request.user,
            is_deleted=False
        ).first()

        if not resume:
            return Response(
                {"error": "Resume not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        version = ResumeVersion.objects.filter(
            resume=resume,
            version_number=version_number
        ).first()

        if not version:
            return Response(
                {"error": "Version not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Restore from snapshot
        snapshot = version.snapshot_data
        resume.title = snapshot.get('title', resume.title)
        resume.save()

        # Clear and restore related data
        resume.educations.all().delete()
        resume.experiences.all().delete()
        resume.skills.all().delete()
        resume.projects.all().delete()

        for edu in snapshot.get('educations', []):
            Education.objects.create(
                resume=resume,
                degree=edu.get('degree'),
                institution=edu.get('institution'),
                start_year=edu.get('start_year'),
                end_year=edu.get('end_year')
            )

        for exp in snapshot.get('experiences', []):
            Experience.objects.create(
                resume=resume,
                company=exp.get('company'),
                role=exp.get('role'),
                start_date=exp.get('start_date'),
                end_date=exp.get('end_date'),
                description=exp.get('description')
            )

        for skill in snapshot.get('skills', []):
            Skill.objects.create(resume=resume, name=skill.get('name'))

        for proj in snapshot.get('projects', []):
            Project.objects.create(
                resume=resume,
                title=proj.get('title'),
                description=proj.get('description'),
                tech_stack=proj.get('tech_stack'),
                project_link=proj.get('project_link', '')
            )

        serializer = ResumeSerializer(resume)
        return Response(serializer.data)


# Public Resume Sharing View
class PublicResumeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, share_code):
        resume = Resume.objects.filter(
            share_code=share_code,
            is_deleted=False
        ).first()

        if not resume:
            return Response(
                {"error": "Resume not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ResumeSerializer(resume)
        return Response(serializer.data)


class GenerateShareLinkView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, resume_id):
        resume = Resume.objects.filter(
            id=resume_id,
            user=request.user,
            is_deleted=False
        ).first()

        if not resume:
            return Response(
                {"error": "Resume not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Generate new share code if not exists
        if not resume.share_code:
            resume.share_code = uuid.uuid4()
            resume.save()

        return Response({
            "share_code": str(resume.share_code),
            "share_url": f"/api/resumes/public/{resume.share_code}/"
        })


class RevokeShareLinkView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, resume_id):
        resume = Resume.objects.filter(
            id=resume_id,
            user=request.user,
            is_deleted=False
        ).first()

        if not resume:
            return Response(
                {"error": "Resume not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        resume.share_code = None
        resume.save()

        return Response({"message": "Share link revoked"})
