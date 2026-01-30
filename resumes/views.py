from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Resume, Education, Experience, Skill, Project
from .serializers import ResumeSerializer, EducationSerializer, ExperienceSerializer, SkillSerializer, ProjectSerializer

class ResumeListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        resumes = Resume.objects.filter(user=request.user)
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
                user=request.user
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
                resume__user=request.user
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
                resume__user=request.user
            )
        except Education.DoesNotExist:
            return Response(
                {"error": "Education not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        education.delete()
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
                user=request.user
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
                resume__user=request.user
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
                resume__user=request.user
            )
        except Experience.DoesNotExist:
            return Response(
                {"error": "Experience not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        experience.delete()
        return Response(
            {"message": "Experience deleted"},
            status=status.HTTP_204_NO_CONTENT
        )

class SkillCreateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, resume_id):
        resume = Resume.objects.filter(
            id=resume_id,
            user=request.user
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
            resume__user=request.user
        ).first()

        if not skill:
            return Response(
                {"error": "Skill not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        skill.delete()
        return Response(
            {"message": "Skill deleted"},
            status=status.HTTP_204_NO_CONTENT
        )
        
class ProjectCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, resume_id):
        resume = Resume.objects.filter(
            id=resume_id,
            user=request.user
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


class ResumeDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, resume_id):
        try:
            resume = Resume.objects.get(
                id=resume_id,
                user=request.user
            )
        except Resume.DoesNotExist:
            return Response(
                {"error": "Resume not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ResumeSerializer(resume)
        return Response(serializer.data)
