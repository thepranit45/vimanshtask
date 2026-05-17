"""
Management command to seed the database with sample data.
Usage: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from jobs.models import Job, Skill
from candidates.models import Application
from accounts.models import UserProfile


class Command(BaseCommand):
    help = 'Seeds the database with sample jobs, skills, and candidates'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # Create recruiter user
        user, created = User.objects.get_or_create(username='recruiter')
        if created:
            user.set_password('recruiter123')
            user.email = 'recruiter@vimansh.com'
            user.save()
            UserProfile.objects.get_or_create(user=user)
            self.stdout.write(self.style.SUCCESS('OK Created user: recruiter / recruiter123'))

        # Create skills
        skill_names = [
            'python', 'django', 'rest api', 'sql', 'postgresql',
            'javascript', 'react', 'nodejs', 'html', 'css',
            'docker', 'git', 'aws', 'linux', 'mongodb',
            'machine learning', 'data analysis', 'pandas', 'numpy', 'fastapi'
        ]
        skills = {}
        for name in skill_names:
            skill, _ = Skill.objects.get_or_create(name=name)
            skills[name] = skill
        self.stdout.write(self.style.SUCCESS(f'+ Created {len(skills)} skills'))

        # Create Jobs
        jobs_data = [
            {
                'title': 'Backend Developer (Django)',
                'description': 'Build and maintain RESTful APIs using Django and Django REST Framework. Work with PostgreSQL databases and ensure clean, tested code.',
                'required_skills': ['python', 'django', 'rest api', 'sql', 'git'],
            },
            {
                'title': 'Full Stack Engineer',
                'description': 'Join our team to build modern web applications with React frontend and Node.js/Django backend.',
                'required_skills': ['javascript', 'react', 'nodejs', 'html', 'css', 'git'],
            },
            {
                'title': 'Data Engineer',
                'description': 'Work with large datasets, build data pipelines, and optimize SQL queries for analytics.',
                'required_skills': ['python', 'sql', 'pandas', 'data analysis', 'aws'],
            },
        ]

        created_jobs = []
        for jd in jobs_data:
            job, created = Job.objects.get_or_create(
                title=jd['title'],
                defaults={'description': jd['description'], 'posted_by': user, 'status': 'open'}
            )
            job.required_skills.set([skills[s] for s in jd['required_skills']])
            created_jobs.append(job)
            if created:
                self.stdout.write(f'  + Job: {job.title}')

        # Create sample candidates
        candidates_data = [
            {
                'job_idx': 0,
                'name': 'Alice Johnson',
                'email': 'alice@example.com',
                'skills': ['python', 'django', 'rest api', 'sql', 'git', 'docker'],
            },
            {
                'job_idx': 0,
                'name': 'Bob Smith',
                'email': 'bob@example.com',
                'skills': ['python', 'django', 'git'],
            },
            {
                'job_idx': 0,
                'name': 'Carol White',
                'email': 'carol@example.com',
                'skills': ['javascript', 'html', 'css'],
            },
            {
                'job_idx': 1,
                'name': 'David Lee',
                'email': 'david@example.com',
                'skills': ['javascript', 'react', 'nodejs', 'html', 'css', 'git'],
            },
            {
                'job_idx': 1,
                'name': 'Emma Davis',
                'email': 'emma@example.com',
                'skills': ['javascript', 'react', 'html'],
            },
            {
                'job_idx': 2,
                'name': 'Frank Chen',
                'email': 'frank@example.com',
                'skills': ['python', 'sql', 'pandas', 'data analysis', 'aws', 'numpy'],
            },
        ]

        for cd in candidates_data:
            job = created_jobs[cd['job_idx']]
            if Application.objects.filter(job=job, email=cd['email']).exists():
                continue
            app = Application(job=job, name=cd['name'], email=cd['email'])
            app.save()
            app.skills.set([skills[s] for s in cd['skills'] if s in skills])
            app.calculate_score()
            app.generate_summary()
            app.save()

            from notifications.models import Notification
            Notification.objects.get_or_create(
                user=user,
                application_id=app.id,
                defaults={
                    'message': f"New application from {app.name} for '{job.title}' - Score: {app.score:.1f}%",
                    'job_title': job.title,
                    'candidate_name': app.name,
                }
            )
            self.stdout.write(f'  + Candidate: {app.name} - {job.title} ({app.score:.1f}%)')

        self.stdout.write(self.style.SUCCESS('\nDONE: Database seeded successfully!'))
        self.stdout.write(self.style.WARNING('\nLogin credentials:'))
        self.stdout.write('  Username: recruiter')
        self.stdout.write('  Password: recruiter123')
        self.stdout.write('  URL: http://127.0.0.1:8000/login/')
