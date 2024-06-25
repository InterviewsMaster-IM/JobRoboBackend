from rest_framework import serializers
from .models import JobBoard, JobRobo, JobType
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class JobBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobBoard
        fields = ['id', 'name']


class JobTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobType
        fields = ['id', 'name']


class JobRoboSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    job_types = JobTypeSerializer(many=True, read_only=True)
    job_board = JobBoardSerializer(read_only=True)

    class Meta:
        model = JobRobo
        fields = ['id', 'user', 'uid', 'job_title', 'job_types', 'location',
                  'number_of_jobs_to_apply', 'created', 'updated', 'job_board']
