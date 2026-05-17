"""Views for the Jobs app (API)."""
from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Job, Skill
from .serializers import JobSerializer, JobListSerializer, SkillSerializer
from candidates.serializers import ApplicationListSerializer


class SkillListCreateView(generics.ListCreateAPIView):
    """List all skills or create a new skill."""
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class JobListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/jobs/         - List all open jobs (public)
    POST /api/jobs/         - Create a job (authenticated)
    Supports: ?search=title, ?status=open, ?skill=python
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'required_skills__name']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = Job.objects.prefetch_related('required_skills', 'applications')
        status_filter = self.request.query_params.get('status')
        skill_filter = self.request.query_params.get('skill')
        if status_filter:
            qs = qs.filter(status=status_filter)
        if skill_filter:
            qs = qs.filter(required_skills__name__icontains=skill_filter)
        return qs

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return JobListSerializer
        return JobSerializer

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)


class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/jobs/{id}/  - Get job details
    PUT    /api/jobs/{id}/  - Update job (authenticated owner)
    DELETE /api/jobs/{id}/  - Delete job (authenticated owner)
    """
    queryset = Job.objects.prefetch_related('required_skills', 'applications')
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class JobCandidatesView(APIView):
    """
    GET /api/jobs/{id}/candidates/
    Returns candidates for this job, sorted by score descending.
    Supports: ?score_min=X  for filtering, ?search=name, ?page=N
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        job = get_object_or_404(Job, pk=pk)
        applications = job.applications.prefetch_related('skills').order_by('-score', '-applied_at')

        score_min = request.query_params.get('score_min')
        if score_min:
            try:
                applications = applications.filter(score__gte=float(score_min))
            except ValueError:
                pass

        search = request.query_params.get('search')
        if search:
            applications = applications.filter(name__icontains=search)

        serializer = ApplicationListSerializer(applications, many=True)
        return Response({
            'job_id': job.id,
            'job_title': job.title,
            'total_candidates': applications.count(),
            'candidates': serializer.data
        })
