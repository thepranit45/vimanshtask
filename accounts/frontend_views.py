"""Frontend (template-based) views for the web UI."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Avg, Count

from jobs.models import Job, Skill
from candidates.models import Application
from notifications.models import Notification
from .models import UserProfile


def _get_role(user):
    """Return the user's role or 'recruiter' by default."""
    try:
        return user.profile.role
    except Exception:
        return 'recruiter'


# ─────────────────────────────────────────
#  AUTH VIEWS
# ─────────────────────────────────────────

def login_view(request):
    """Shared login page — redirects recruiter vs candidate after login."""
    if request.user.is_authenticated:
        role = _get_role(request.user)
        return redirect('candidate-portal-dashboard' if role == 'candidate' else 'dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            role = _get_role(user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('candidate-portal-dashboard' if role == 'candidate' else 'dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def register_view(request):
    """Recruiter registration page."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm = request.POST.get('confirm_password', '')
        if password != confirm:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            UserProfile.objects.create(user=user, role='recruiter')
            login(request, user)
            messages.success(request, f'Welcome, {username}! Account created.')
            return redirect('dashboard')
    return render(request, 'register.html')


def candidate_register_view(request):
    """Candidate-specific registration page."""
    if request.user.is_authenticated:
        return redirect('candidate-portal-dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm = request.POST.get('confirm_password', '')
        if not username or not email:
            messages.error(request, 'Username and email are required.')
        elif password != confirm:
            messages.error(request, 'Passwords do not match.')
        elif len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        elif User.objects.filter(email__iexact=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            UserProfile.objects.create(user=user, role='candidate')
            login(request, user)
            messages.success(request, f'Welcome, {username}! Your candidate account is ready.')
            return redirect('candidate-portal-dashboard')
    return render(request, 'candidate/register.html')


def logout_view(request):
    """Logout and redirect to login."""
    logout(request)
    return redirect('login')


# ─────────────────────────────────────────
#  RECRUITER VIEWS
# ─────────────────────────────────────────

def recruiter_required(view_func):
    """Decorator: redirects candidates away from recruiter pages."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if _get_role(request.user) == 'candidate':
            return redirect('candidate-portal-dashboard')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


@recruiter_required
def dashboard_view(request):
    """Recruiter dashboard."""
    jobs = Job.objects.filter(posted_by=request.user).annotate(
        app_count=Count('applications')
    ).order_by('-created_at')[:5]

    total_jobs = Job.objects.filter(posted_by=request.user).count()
    total_applications = Application.objects.filter(job__posted_by=request.user).count()
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False).count()
    avg_score = Application.objects.filter(job__posted_by=request.user).aggregate(
        avg=Avg('score')
    )['avg'] or 0

    recent_applications = Application.objects.filter(
        job__posted_by=request.user
    ).select_related('job').order_by('-applied_at')[:5]

    return render(request, 'dashboard.html', {
        'jobs': jobs,
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'unread_notifications': unread_notifications,
        'avg_score': round(avg_score, 1),
        'recent_applications': recent_applications,
    })


@recruiter_required
def job_list_view(request):
    """Job listing page."""
    jobs = Job.objects.filter(posted_by=request.user).annotate(
        app_count=Count('applications')
    ).order_by('-created_at')
    skills = Skill.objects.all()
    return render(request, 'jobs/list.html', {'jobs': jobs, 'skills': skills})


@recruiter_required
def job_detail_view(request, pk):
    """Job detail page with candidates."""
    job = get_object_or_404(Job, pk=pk, posted_by=request.user)
    score_min = request.GET.get('score_min', 0)
    search = request.GET.get('search', '')

    applications = job.applications.prefetch_related('skills').order_by('-score')
    if score_min:
        try:
            applications = applications.filter(score__gte=float(score_min))
        except ValueError:
            pass
    if search:
        applications = applications.filter(name__icontains=search)

    return render(request, 'jobs/detail.html', {
        'job': job,
        'applications': applications,
        'score_min': score_min,
        'search': search,
    })


@recruiter_required
def candidate_list_view(request):
    """Candidate listing page with scores."""
    applications = Application.objects.filter(
        job__posted_by=request.user
    ).select_related('job').prefetch_related('skills').order_by('-score')

    score_min = request.GET.get('score_min', '')
    job_filter = request.GET.get('job_id', '')
    search = request.GET.get('search', '')

    if score_min:
        try:
            applications = applications.filter(score__gte=float(score_min))
        except ValueError:
            pass
    if job_filter:
        applications = applications.filter(job_id=job_filter)
    if search:
        applications = applications.filter(name__icontains=search)

    jobs = Job.objects.filter(posted_by=request.user).values('id', 'title')
    return render(request, 'candidates/list.html', {
        'applications': applications,
        'jobs': jobs,
        'score_min': score_min,
        'job_filter': job_filter,
        'search': search,
    })


@recruiter_required
def notification_list_view(request):
    """Notification display page."""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()
    return render(request, 'notifications/list.html', {
        'notifications': notifications,
        'unread_count': unread_count,
    })


# ─────────────────────────────────────────
#  CANDIDATE PORTAL VIEWS
# ─────────────────────────────────────────

def candidate_required(view_func):
    """Decorator: only allows candidate-role users."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('candidate-login')
        if _get_role(request.user) != 'candidate':
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


@candidate_required
def candidate_portal_dashboard(request):
    """Candidate's personal dashboard: open jobs + their applications."""
    open_jobs = Job.objects.filter(status='open').prefetch_related('required_skills').order_by('-created_at')
    my_applications = Application.objects.filter(
        email__iexact=request.user.email
    ).select_related('job').prefetch_related('skills').order_by('-applied_at')

    search = request.GET.get('search', '')
    if search:
        open_jobs = open_jobs.filter(title__icontains=search)

    return render(request, 'candidate/dashboard.html', {
        'open_jobs': open_jobs,
        'my_applications': my_applications,
        'search': search,
        'total_applied': my_applications.count(),
        'best_score': my_applications.order_by('-score').first(),
    })


@candidate_required
def candidate_portal_jobs(request):
    """Browse all open jobs as a candidate."""
    jobs = Job.objects.filter(status='open').prefetch_related('required_skills').order_by('-created_at')
    search = request.GET.get('search', '')
    skill_filter = request.GET.get('skill', '')

    if search:
        jobs = jobs.filter(title__icontains=search)
    if skill_filter:
        jobs = jobs.filter(required_skills__name__icontains=skill_filter)

    # Mark which ones the candidate has already applied to
    applied_job_ids = set(
        Application.objects.filter(email__iexact=request.user.email).values_list('job_id', flat=True)
    )

    return render(request, 'candidate/jobs.html', {
        'jobs': jobs,
        'applied_job_ids': applied_job_ids,
        'search': search,
        'skill_filter': skill_filter,
    })


@candidate_required
def candidate_portal_my_applications(request):
    """Candidate's submitted applications with scores."""
    applications = Application.objects.filter(
        email__iexact=request.user.email
    ).select_related('job').prefetch_related('skills').order_by('-score', '-applied_at')

    return render(request, 'candidate/my_applications.html', {
        'applications': applications,
    })


# ─────────────────────────────────────────
#  PUBLIC APPLY VIEWS (no login required)
# ─────────────────────────────────────────

def apply_public_view(request, job_id):
    """Public-facing job application form."""
    job = get_object_or_404(Job, pk=job_id, status='open')

    # Pre-fill from logged-in candidate
    prefill = {}
    if request.user.is_authenticated and _get_role(request.user) == 'candidate':
        prefill = {'name': request.user.get_full_name() or request.user.username,
                   'email': request.user.email}

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        skill_names = request.POST.get('skill_names', '')
        resume = request.FILES.get('resume')

        if Application.objects.filter(job=job, email__iexact=email).exists():
            messages.error(request, 'You have already applied for this job.')
            return redirect('apply-public', job_id=job_id)

        skill_list = [s.strip() for s in skill_names.split(',') if s.strip()]
        application = Application(job=job, name=name, email=email.lower())
        if resume:
            application.resume = resume
        application.save()

        skills = []
        for sname in skill_list:
            skill, _ = Skill.objects.get_or_create(name=sname.lower())
            skills.append(skill)
        application.skills.set(skills)

        application.calculate_score()
        application.generate_summary()
        application.save()

        Notification.objects.create(
            user=job.posted_by,
            message=f"New application from {name} for '{job.title}' - Score: {application.score:.1f}%",
            application_id=application.id,
            job_title=job.title,
            candidate_name=name,
        )

        messages.success(request, f'Application submitted! Your match score: {application.score:.1f}%')
        return redirect('apply-success', job_id=job_id)

    return render(request, 'apply.html', {'job': job, 'prefill': prefill})


def apply_success_view(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    return render(request, 'apply_success.html', {'job': job})
