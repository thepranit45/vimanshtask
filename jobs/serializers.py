"""Serializers for the Jobs app."""
from rest_framework import serializers
from .models import Job, Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']


class JobSerializer(serializers.ModelSerializer):
    required_skills = SkillSerializer(many=True, read_only=True)
    required_skill_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Skill.objects.all(), write_only=True, source='required_skills'
    )
    required_skill_names = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )
    posted_by_username = serializers.ReadOnlyField(source='posted_by.username')
    application_count = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'required_skills',
            'required_skill_ids', 'required_skill_names',
            'posted_by', 'posted_by_username', 'status',
            'application_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['posted_by', 'created_at', 'updated_at']

    def get_application_count(self, obj):
        return obj.applications.count()

    def create(self, validated_data):
        skill_names = validated_data.pop('required_skill_names', [])
        skills_from_ids = validated_data.pop('required_skills', [])

        job = Job.objects.create(**validated_data)

        # Handle skill names (create if not exists)
        all_skills = list(skills_from_ids)
        for name in skill_names:
            skill, _ = Skill.objects.get_or_create(name=name.strip().lower())
            all_skills.append(skill)

        job.required_skills.set(all_skills)
        return job

    def update(self, instance, validated_data):
        skill_names = validated_data.pop('required_skill_names', [])
        skills_from_ids = validated_data.pop('required_skills', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if skills_from_ids is not None or skill_names:
            all_skills = list(skills_from_ids or [])
            for name in skill_names:
                skill, _ = Skill.objects.get_or_create(name=name.strip().lower())
                all_skills.append(skill)
            instance.required_skills.set(all_skills)

        return instance


class JobListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for job listing."""
    required_skills = SkillSerializer(many=True, read_only=True)
    application_count = serializers.SerializerMethodField()
    posted_by_username = serializers.ReadOnlyField(source='posted_by.username')

    class Meta:
        model = Job
        fields = ['id', 'title', 'status', 'required_skills', 'application_count',
                  'posted_by_username', 'created_at']

    def get_application_count(self, obj):
        return obj.applications.count()
