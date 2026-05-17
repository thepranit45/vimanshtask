"""Views for the Candidates app (API)."""
import os
import io
from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from .models import Application
from .serializers import ApplicationSerializer, ApplicationListSerializer
from jobs.models import Job, Skill
from notifications.models import Notification


def parse_resume(file):
    """Extract text from uploaded resume (PDF or DOCX)."""
    extracted_skills = []
    try:
        name = file.name.lower()
        content = file.read()
        file.seek(0)

        text = ""
        if name.endswith('.pdf'):
            try:
                import PyPDF2
                reader = PyPDF2.PdfReader(io.BytesIO(content))
                for page in reader.pages:
                    text += page.extract_text() or ""
            except Exception:
                pass
        elif name.endswith('.docx'):
            try:
                import docx
                doc = docx.Document(io.BytesIO(content))
                text = "\n".join([p.text for p in doc.paragraphs])
            except Exception:
                pass
        else:
            text = content.decode('utf-8', errors='ignore')

        # Simple keyword skill extraction
        all_skills = list(Skill.objects.values_list('name', flat=True))
        text_lower = text.lower()
        for skill_name in all_skills:
            if skill_name.lower() in text_lower:
                extracted_skills.append(skill_name)

    except Exception:
        pass
    return extracted_skills


class ApplicationPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ApplyForJobView(APIView):
    """
    POST /api/jobs/{job_id}/apply/
    Candidate applies for a job. Score is auto-calculated.
    Notification is sent to job poster.
    """
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request, job_id):
        job = get_object_or_404(Job, pk=job_id)

        if job.status != 'open':
            return Response(
                {'error': f"Job '{job.title}' is not accepting applications (status: {job.status})."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Prevent duplicate applications
        email = request.data.get('email', '').strip().lower()
        if Application.objects.filter(job=job, email__iexact=email).exists():
            return Response(
                {'error': 'You have already applied for this job with this email.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Handle skills: comma-separated string or list
        skill_names = request.data.get('skill_names', [])
        if isinstance(skill_names, str):
            skill_names = [s.strip() for s in skill_names.split(',') if s.strip()]

        # Auto-extract skills from resume if uploaded
        resume_file = request.FILES.get('resume')
        resume_extracted = []
        if resume_file:
            resume_extracted = parse_resume(resume_file)
            resume_file.seek(0)

        # Merge manually provided skills + resume-extracted skills
        all_skill_names = list(set(skill_names + resume_extracted))

        # Build application data
        data = {
            'name': request.data.get('name', ''),
            'email': email,
            'skill_names': all_skill_names,
        }

        serializer = ApplicationSerializer(data=data)
        if serializer.is_valid():
            application = serializer.save(job=job)

            # Create notification for job poster
            Notification.objects.create(
                user=job.posted_by,
                message=f"New application from {application.name} for '{job.title}' — Score: {application.score:.1f}%",
                application_id=application.id,
                job_title=job.title,
                candidate_name=application.name,
            )

            return Response({
                'message': 'Application submitted successfully!',
                'application': ApplicationSerializer(application).data,
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicationListView(generics.ListAPIView):
    """
    GET /api/candidates/
    List all applications with pagination, filtering, and search.
    ?job_id=X, ?score_min=X, ?search=name, ?status=pending
    """
    serializer_class = ApplicationListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ApplicationPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email', 'job__title']
    ordering_fields = ['score', 'applied_at', 'name']
    ordering = ['-score']

    def get_queryset(self):
        qs = Application.objects.select_related('job').prefetch_related('skills')

        job_id = self.request.query_params.get('job_id')
        score_min = self.request.query_params.get('score_min')
        app_status = self.request.query_params.get('status')

        if job_id:
            qs = qs.filter(job_id=job_id)
        if score_min:
            try:
                qs = qs.filter(score__gte=float(score_min))
            except ValueError:
                pass
        if app_status:
            qs = qs.filter(status=app_status)

        return qs


class ApplicationDetailView(generics.RetrieveUpdateAPIView):
    """
    GET   /api/candidates/{id}/  - Get application detail
    PATCH /api/candidates/{id}/  - Update status
    """
    queryset = Application.objects.select_related('job').prefetch_related('skills')
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
