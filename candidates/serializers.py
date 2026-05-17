"""Serializers for the Candidates app."""
from rest_framework import serializers
from .models import Application
from jobs.models import Skill
from jobs.serializers import SkillSerializer


class ApplicationSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    skill_names = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )
    job_title = serializers.ReadOnlyField(source='job.title')
    job_id = serializers.ReadOnlyField(source='job.id')

    class Meta:
        model = Application
        fields = [
            'id', 'job', 'job_id', 'job_title', 'name', 'email',
            'skills', 'skill_names', 'resume', 'score', 'summary',
            'status', 'applied_at'
        ]
        read_only_fields = ['score', 'summary', 'applied_at', 'job']

    def create(self, validated_data):
        skill_names = validated_data.pop('skill_names', [])
        application = Application.objects.create(**validated_data)

        # Resolve skills by name (create if not exists)
        skills = []
        for name in skill_names:
            skill, _ = Skill.objects.get_or_create(name=name.strip().lower())
            skills.append(skill)
        application.skills.set(skills)

        # Calculate score and generate summary
        application.calculate_score()
        application.generate_summary()
        application.save()

        return application


class ApplicationListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing candidates."""
    skills = SkillSerializer(many=True, read_only=True)
    job_title = serializers.ReadOnlyField(source='job.title')

    class Meta:
        model = Application
        fields = [
            'id', 'name', 'email', 'job_title', 'skills',
            'score', 'status', 'applied_at', 'summary'
        ]
