from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User
from .models import Resume, Education, Experience, Skill, Project, CoverLetter, JobApplication, ResumeVersion, ResumeAnalytics
import json
import uuid


class ResumeCRUDTests(TestCase):
    """Test resume CRUD operations"""

    def setUp(self):
        self.client = APIClient()
        self.resumes_list_url = '/api/resumes/'

        # Create two users for isolation testing
        self.user_a = User.objects.create_user(
            username='usera',
            password='TestPass123!',
            email='usera@example.com'
        )
        self.user_b = User.objects.create_user(
            username='userb',
            password='TestPass123!',
            email='userb@example.com'
        )

        # Login as User A
        login_response = self.client.post('/api/accounts/login/', {
            'username': 'usera',
            'password': 'TestPass123!'
        }, format='json')
        self.token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Create a test resume
        self.resume = Resume.objects.create(
            user=self.user_a,
            title='Test Resume'
        )

    def test_create_resume_valid(self):
        """RES-001: Create resume with valid data should work"""
        data = {'title': 'Software Engineer Resume'}
        response = self.client.post(self.resumes_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Resume.objects.filter(user=self.user_a).count(), 2)

    def test_create_resume_empty_title(self):
        """RES-002: Empty title should be rejected"""
        data = {'title': ''}
        response = self.client.post(self.resumes_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_resume_list(self):
        """RES-005: Get resume list should return user's resumes"""
        response = self.client.get(self.resumes_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_resume(self):
        """RES-007: Get single resume should return full data"""
        url = f'/api/resumes/{self.resume.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Resume')

    def test_resume_isolation(self):
        """RES-006: User should only see own resumes"""
        # Create resume for User B
        Resume.objects.create(user=self.user_b, title='User B Resume')

        # User A should only see 1 resume (their own)
        response = self.client.get(self.resumes_list_url)
        self.assertEqual(len(response.data), 1)

    def test_update_resume_own(self):
        """RES-009: Update own resume should work"""
        url = f'/api/resumes/{self.resume.id}/'
        data = {'title': 'Updated Resume Title'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.resume.refresh_from_db()
        self.assertEqual(self.resume.title, 'Updated Resume Title')

    def test_update_resume_another_user(self):
        """RES-010: Update another user's resume should fail"""
        # Create resume for User B
        user_b_resume = Resume.objects.create(user=self.user_b, title='User B Resume')
        url = f'/api/resumes/{user_b_resume.id}/'
        data = {'title': 'Hacked Title'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_resume(self):
        """RES-011: Delete resume should soft delete"""
        url = f'/api/resumes/{self.resume.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Verify soft delete
        self.resume.refresh_from_db()
        self.assertTrue(self.resume.is_deleted)

    def test_access_deleted_resume(self):
        """RES-014: Deleted resume should not be accessible"""
        self.resume.is_deleted = True
        self.resume.save()

        url = f'/api/resumes/{self.resume.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class EducationCRUDTests(TestCase):
    """Test education CRUD operations"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPass123!'
        )
        self.resume = Resume.objects.create(user=self.user, title='Test Resume')

        login_response = self.client.post('/api/accounts/login/', {
            'username': 'testuser',
            'password': 'TestPass123!'
        }, format='json')
        self.token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_education_valid(self):
        """EDU-001: Create education with valid data should work"""
        data = {
            'degree': 'Bachelor of Science',
            'institution': 'MIT',
            'start_year': 2018,
            'end_year': 2022
        }
        url = f'/api/resumes/{self.resume.id}/education/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Education.objects.filter(resume=self.resume).count(), 1)

    def test_create_education_missing_degree(self):
        """EDU-002: Missing degree should be rejected"""
        data = {
            'degree': '',
            'institution': 'MIT',
            'start_year': 2018,
            'end_year': 2022
        }
        url = f'/api/resumes/{self.resume.id}/education/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_education_end_before_start(self):
        """EDU-005: End year before start year should be rejected"""
        data = {
            'degree': 'Bachelor of Science',
            'institution': 'MIT',
            'start_year': 2022,
            'end_year': 2018
        }
        url = f'/api/resumes/{self.resume.id}/education/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_education_empty_end_year(self):
        """EDU-007: Empty end year should work (nullable)"""
        data = {
            'degree': 'Bachelor of Science',
            'institution': 'MIT',
            'start_year': 2018,
            'end_year': None
        }
        url = f'/api/resumes/{self.resume.id}/education/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_education(self):
        """EDU-008: Update education should work"""
        # Create education
        edu = Education.objects.create(
            resume=self.resume,
            degree='Bachelor',
            institution='MIT',
            start_year=2018,
            end_year=2022
        )
        url = f'/api/resumes/education/{edu.id}/'
        data = {'degree': 'Master'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        edu.refresh_from_db()
        self.assertEqual(edu.degree, 'Master')

    def test_delete_education_soft(self):
        """EDU-010: Delete education should soft delete"""
        edu = Education.objects.create(
            resume=self.resume,
            degree='Bachelor',
            institution='MIT',
            start_year=2018,
            end_year=2022
        )
        url = f'/api/resumes/education/{edu.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        edu.refresh_from_db()
        self.assertTrue(edu.is_deleted)

    def test_education_idor(self):
        """EDU-013: IDOR - Cannot access another user's education"""
        # Create another user and education
        other_user = User.objects.create_user(username='otheruser', password='TestPass123!')
        other_resume = Resume.objects.create(user=other_user, title='Other Resume')
        other_edu = Education.objects.create(
            resume=other_resume,
            degree='Bachelor',
            institution='Other University',
            start_year=2018,
            end_year=2022
        )

        url = f'/api/resumes/education/{other_edu.id}/'
        response = self.client.patch(url, {'degree': 'Hacked'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ExperienceCRUDTests(TestCase):
    """Test experience CRUD operations"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPass123!'
        )
        self.resume = Resume.objects.create(user=self.user, title='Test Resume')

        login_response = self.client.post('/api/accounts/login/', {
            'username': 'testuser',
            'password': 'TestPass123!'
        }, format='json')
        self.token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_experience_valid(self):
        """EXP-001: Create experience with valid data should work"""
        data = {
            'company': 'Google',
            'role': 'Software Engineer',
            'start_date': '2020-01-01',
            'end_date': '2022-01-01',
            'description': 'Worked on various projects'
        }
        url = f'/api/resumes/{self.resume.id}/experience/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_experience_end_before_start(self):
        """EXP-004: End date before start date should be rejected"""
        data = {
            'company': 'Google',
            'role': 'Software Engineer',
            'start_date': '2022-01-01',
            'end_date': '2020-01-01',
            'description': 'Worked on various projects'
        }
        url = f'/api/resumes/{self.resume.id}/experience/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_experience_null_end_date(self):
        """EXP-007: Null end date (present) should work"""
        data = {
            'company': 'Google',
            'role': 'Software Engineer',
            'start_date': '2020-01-01',
            'end_date': None,
            'description': 'Working here'
        }
        url = f'/api/resumes/{self.resume.id}/experience/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class SkillCRUDTests(TestCase):
    """Test skill CRUD operations"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPass123!'
        )
        self.resume = Resume.objects.create(user=self.user, title='Test Resume')

        login_response = self.client.post('/api/accounts/login/', {
            'username': 'testuser',
            'password': 'TestPass123!'
        }, format='json')
        self.token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_skill_valid(self):
        """SKL-001: Create skill with valid data should work"""
        data = {'name': 'Python'}
        url = f'/api/resumes/{self.resume.id}/skills/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_skill_empty_name(self):
        """SKL-002: Empty skill name should be handled"""
        data = {'name': ''}
        url = f'/api/resumes/{self.resume.id}/skills/'
        response = self.client.post(url, data, format='json')
        # Should either skip or reject
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])

    def test_update_skill(self):
        """SKL-005: Update skill should work"""
        skill = Skill.objects.create(resume=self.resume, name='Python')
        url = f'/api/resumes/skills/{skill.id}/'
        response = self.client.patch(url, {'name': 'Python/Django'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        skill.refresh_from_db()
        self.assertEqual(skill.name, 'Python/Django')

    def test_delete_skill_soft(self):
        """SKL-007: Delete skill should soft delete"""
        skill = Skill.objects.create(resume=self.resume, name='Python')
        url = f'/api/resumes/skills/{skill.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        skill.refresh_from_db()
        self.assertTrue(skill.is_deleted)


class ProjectCRUDTests(TestCase):
    """Test project CRUD operations"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPass123!'
        )
        self.resume = Resume.objects.create(user=self.user, title='Test Resume')

        login_response = self.client.post('/api/accounts/login/', {
            'username': 'testuser',
            'password': 'TestPass123!'
        }, format='json')
        self.token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_project_valid(self):
        """PRJ-001: Create project with valid data should work"""
        data = {
            'title': 'E-commerce Website',
            'description': 'Built a full-stack e-commerce platform',
            'tech_stack': 'React, Node.js, MongoDB',
            'project_link': 'https://github.com/user/project'
        }
        url = f'/api/resumes/{self.resume.id}/projects/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_project_missing_title(self):
        """PRJ-002: Missing title should be rejected"""
        data = {
            'title': '',
            'description': 'Some project',
            'tech_stack': 'React',
            'project_link': ''
        }
        url = f'/api/resumes/{self.resume.id}/projects/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_project_soft(self):
        """PRJ-007: Delete project should soft delete"""
        project = Project.objects.create(
            resume=self.resume,
            title='Test Project',
            description='Test Description',
            tech_stack='React'
        )
        url = f'/api/resumes/projects/{project.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        project.refresh_from_db()
        self.assertTrue(project.is_deleted)


class SharingTests(TestCase):
    """Test public sharing functionality"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPass123!'
        )
        self.resume = Resume.objects.create(user=self.user, title='Test Resume')

        login_response = self.client.post('/api/accounts/login/', {
            'username': 'testuser',
            'password': 'TestPass123!'
        }, format='json')
        self.token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_generate_share_link(self):
        """SHR-001: Generate share link should work"""
        url = f'/api/resumes/{self.resume.id}/share/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('share_code', response.data)
        self.resume.refresh_from_db()
        self.assertIsNotNone(self.resume.share_code)

    def test_revoke_share_link(self):
        """SHR-006: Revoke share link should work"""
        # Generate link first
        self.resume.share_code = uuid.uuid4()
        self.resume.save()

        url = f'/api/resumes/{self.resume.id}/share/revoke/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.resume.refresh_from_db()
        self.assertIsNone(self.resume.share_code)

    def test_public_resume_access(self):
        """SHR-002: Public resume should be accessible without auth"""
        self.resume.share_code = uuid.uuid4()
        self.resume.save()

        self.client.credentials()  # Remove auth
        url = f'/api/resumes/public/{self.resume.share_code}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_public_resume_invalid_uuid(self):
        """SHR-004: Invalid UUID should return 404"""
        self.client.credentials()
        url = '/api/resumes/public/invalid-uuid/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_public_resume_deleted(self):
        """SHR-005: Deleted resume should not be accessible via share link"""
        self.resume.share_code = uuid.uuid4()
        self.resume.is_deleted = True
        self.resume.save()

        self.client.credentials()
        url = f'/api/resumes/public/{self.resume.share_code}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CoverLetterTests(TestCase):
    """Test cover letter CRUD operations"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPass123!'
        )
        self.resume = Resume.objects.create(user=self.user, title='Test Resume')

        login_response = self.client.post('/api/accounts/login/', {
            'username': 'testuser',
            'password': 'TestPass123!'
        }, format='json')
        self.token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_cover_letter_valid(self):
        """CL-001: Create cover letter with valid data should work"""
        data = {
            'title': 'Software Engineer Cover Letter',
            'content': 'Dear Hiring Manager,\n\nI am writing to apply...'
        }
        url = f'/api/resumes/{self.resume.id}/cover-letters/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CoverLetter.objects.filter(resume=self.resume).count(), 1)

    def test_create_cover_letter_empty_content(self):
        """CL-002: Empty content should be rejected"""
        data = {
            'title': 'Cover Letter',
            'content': ''
        }
        url = f'/api/resumes/{self.resume.id}/cover-letters/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_cover_letters(self):
        """CL-003: Get cover letters should return list"""
        CoverLetter.objects.create(
            resume=self.resume,
            title='Test Cover Letter',
            content='Test content'
        )
        url = f'/api/resumes/{self.resume.id}/cover-letters/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_cover_letter(self):
        """CL-004: Update cover letter should work"""
        cover_letter = CoverLetter.objects.create(
            resume=self.resume,
            title='Original Title',
            content='Original content'
        )
        url = f'/api/resumes/cover-letters/{cover_letter.id}/'
        data = {'title': 'Updated Title'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cover_letter.refresh_from_db()
        self.assertEqual(cover_letter.title, 'Updated Title')

    def test_delete_cover_letter_soft(self):
        """CL-005: Delete cover letter should soft delete"""
        cover_letter = CoverLetter.objects.create(
            resume=self.resume,
            title='Test Cover Letter',
            content='Test content'
        )
        url = f'/api/resumes/cover-letters/{cover_letter.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        cover_letter.refresh_from_db()
        self.assertTrue(cover_letter.is_deleted)

    def test_cover_letter_idor(self):
        """CL-006: Cannot access another user's cover letter"""
        other_user = User.objects.create_user(username='otheruser', password='TestPass123!')
        other_resume = Resume.objects.create(user=other_user, title='Other Resume')
        other_cover_letter = CoverLetter.objects.create(
            resume=other_resume,
            title='Other Cover Letter',
            content='Other content'
        )

        url = f'/api/resumes/cover-letters/{other_cover_letter.id}/'
        response = self.client.patch(url, {'title': 'Hacked'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class JobApplicationTests(TestCase):
    """Test job application tracking"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPass123!'
        )
        self.resume = Resume.objects.create(user=self.user, title='Test Resume')

        login_response = self.client.post('/api/accounts/login/', {
            'username': 'testuser',
            'password': 'TestPass123!'
        }, format='json')
        self.token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_job_application_valid(self):
        """JOB-001: Create job application with valid data should work"""
        data = {
            'company': 'Google',
            'position': 'Software Engineer',
            'applied_date': '2024-01-15',
            'status': 'applied',
            'job_url': 'https://careers.google.com/jobs/123',
            'notes': 'Referred by John'
        }
        url = f'/api/resumes/{self.resume.id}/jobs/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(JobApplication.objects.filter(resume=self.resume).count(), 1)

    def test_create_job_application_invalid_status(self):
        """JOB-002: Invalid status should be rejected"""
        data = {
            'company': 'Google',
            'position': 'Software Engineer',
            'applied_date': '2024-01-15',
            'status': 'invalid_status'
        }
        url = f'/api/resumes/{self.resume.id}/jobs/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_job_applications(self):
        """JOB-003: Get job applications should return list"""
        JobApplication.objects.create(
            resume=self.resume,
            company='Google',
            position='Software Engineer',
            applied_date='2024-01-15',
            status='applied'
        )
        url = f'/api/resumes/{self.resume.id}/jobs/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_job_application_status(self):
        """JOB-004: Update job application status should work"""
        application = JobApplication.objects.create(
            resume=self.resume,
            company='Google',
            position='Software Engineer',
            applied_date='2024-01-15',
            status='applied'
        )
        url = f'/api/resumes/jobs/{application.id}/'
        data = {'status': 'interviewing'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        application.refresh_from_db()
        self.assertEqual(application.status, 'interviewing')

    def test_delete_job_application(self):
        """JOB-005: Delete job application should work (hard delete)"""
        application = JobApplication.objects.create(
            resume=self.resume,
            company='Google',
            position='Software Engineer',
            applied_date='2024-01-15',
            status='applied'
        )
        url = f'/api/resumes/jobs/{application.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(JobApplication.objects.filter(resume=self.resume).count(), 0)

    def test_job_application_idor(self):
        """JOB-006: Cannot access another user's job application"""
        other_user = User.objects.create_user(username='otheruser', password='TestPass123!')
        other_resume = Resume.objects.create(user=other_user, title='Other Resume')
        other_application = JobApplication.objects.create(
            resume=other_resume,
            company='Google',
            position='Software Engineer',
            applied_date='2024-01-15',
            status='applied'
        )

        url = f'/api/resumes/jobs/{other_application.id}/'
        response = self.client.patch(url, {'status': 'rejected'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ResumeVersioningTests(TestCase):
    """Test resume versioning functionality"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPass123!'
        )
        self.resume = Resume.objects.create(user=self.user, title='Test Resume v1')

        login_response = self.client.post('/api/accounts/login/', {
            'username': 'testuser',
            'password': 'TestPass123!'
        }, format='json')
        self.token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_get_versions_list(self):
        """VER-001: Get versions list should return empty initially"""
        url = f'/api/resumes/{self.resume.id}/versions/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_create_version(self):
        """VER-002: Create version should create snapshot"""
        # Add some data first
        Education.objects.create(
            resume=self.resume,
            degree='Bachelor',
            institution='MIT',
            start_year=2018,
            end_year=2022
        )

        url = f'/api/resumes/{self.resume.id}/versions/create/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ResumeVersion.objects.filter(resume=self.resume).count(), 1)
        self.resume.refresh_from_db()
        self.assertEqual(self.resume.version, 2)

    def test_restore_version(self):
        """VER-003: Restore version should restore snapshot data"""
        # Create version with initial data
        Education.objects.create(
            resume=self.resume,
            degree='Bachelor',
            institution='MIT',
            start_year=2018,
            end_year=2022
        )

        # Create version
        url = f'/api/resumes/{self.resume.id}/versions/create/'
        self.client.post(url)

        # Modify data
        self.resume.title = 'Modified Title'
        self.resume.save()
        Education.objects.all().delete()

        # Restore version 2
        url = f'/api/resumes/{self.resume.id}/versions/2/restore/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.resume.refresh_from_db()
        self.assertEqual(self.resume.title, 'Test Resume v1')
        self.assertEqual(Education.objects.filter(resume=self.resume).count(), 1)

    def test_restore_nonexistent_version(self):
        """VER-004: Restore nonexistent version should fail"""
        url = f'/api/resumes/{self.resume.id}/versions/999/restore/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_version_idor(self):
        """VER-005: Cannot create version for another user's resume"""
        other_user = User.objects.create_user(username='otheruser', password='TestPass123!')
        other_resume = Resume.objects.create(user=other_user, title='Other Resume')

        url = f'/api/resumes/{other_resume.id}/versions/create/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ResumeAnalyticsTests(TestCase):
    """Test resume analytics functionality"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPass123!'
        )
        self.resume = Resume.objects.create(user=self.user, title='Test Resume')

        login_response = self.client.post('/api/accounts/login/', {
            'username': 'testuser',
            'password': 'TestPass123!'
        }, format='json')
        self.token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_get_analytics(self):
        """ANA-001: Get analytics should return analytics data"""
        url = f'/api/resumes/{self.resume.id}/analytics/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('views', response.data)
        self.assertEqual(response.data['views'], 0)

    def test_increment_view(self):
        """ANA-002: Increment view should increase view count"""
        url = f'/api/resumes/{self.resume.id}/analytics/view/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['views'], 1)

        # Increment again
        response = self.client.post(url)
        self.assertEqual(response.data['views'], 2)

    def test_analytics_idor(self):
        """ANA-003: Cannot access another user's analytics"""
        other_user = User.objects.create_user(username='otheruser', password='TestPass123!')
        other_resume = Resume.objects.create(user=other_user, title='Other Resume')

        url = f'/api/resumes/{other_resume.id}/analytics/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
