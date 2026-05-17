"""Models for the Candidates app."""
from django.db import models
from django.contrib.auth.models import User
from jobs.models import Job, Skill


class Application(models.Model):
    """A candidate's application for a specific job."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    skills = models.ManyToManyField(Skill, related_name='applications', blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    score = models.FloatField(default=0.0)
    summary = models.TextField(blank=True, default='')  # AI-generated or parsed
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} → {self.job.title} ({self.score:.1f}%)"

    def calculate_score(self):
        """
        Skill-matching logic:
        Score = (# of matching skills / # of required skills) * 100
        Returns 100 if job has no required skills.
        """
        required = set(self.job.required_skills.values_list('id', flat=True))
        if not required:
            self.score = 100.0
            return 100.0
        candidate_skills = set(self.skills.values_list('id', flat=True))
        matched = required.intersection(candidate_skills)
        score = (len(matched) / len(required)) * 100
        self.score = round(score, 2)
        return self.score

    def generate_summary(self):
        """Generate a basic AI-style summary based on skills and score."""
        required = list(self.job.required_skills.values_list('name', flat=True))
        candidate = list(self.skills.values_list('name', flat=True))
        matched = [s for s in candidate if s in required]
        missing = [s for s in required if s not in candidate]
        extra = [s for s in candidate if s not in required]

        summary_parts = [
            f"{self.name} applied for '{self.job.title}' with a skill match score of {self.score:.1f}%.",
        ]
        if matched:
            summary_parts.append(f"Matching skills: {', '.join(matched)}.")
        if missing:
            summary_parts.append(f"Missing required skills: {', '.join(missing)}.")
        if extra:
            summary_parts.append(f"Additional skills: {', '.join(extra)}.")

        if self.score >= 80:
            summary_parts.append("Strong candidate — highly recommended for interview.")
        elif self.score >= 50:
            summary_parts.append("Moderate fit — worth reviewing further.")
        else:
            summary_parts.append("Low skill match — consider for future openings.")

        self.summary = ' '.join(summary_parts)
        return self.summary

    class Meta:
        ordering = ['-score', '-applied_at']
        # Prevent duplicate applications
        unique_together = [['job', 'email']]
