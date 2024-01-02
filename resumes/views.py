from django.shortcuts import render
from django.utils import timezone
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Resume
from .serializers import ResumeSerializer
from rest_framework.decorators import api_view
from .aiparser import parse_resume_save_in_db_task
from celery.result import AsyncResult
from django.http import JsonResponse


@api_view(['POST'])
def resume_upload(request):
    # Validate the necessary fields
    file = request.data.get('file')
    if not file:
        return Response({'error': 'File is required'}, status=status.HTTP_400_BAD_REQUEST)

    resume = Resume(file=file)
    resume.submitted_at = timezone.now()
    resume.user = request.user  # Assuming you have a user field and the user is logged in
    # ... set other fields as needed
    resume.save()

    # Serialize the resume after saving
    resume_serializer = ResumeSerializer(resume)
    return JsonResponse(resume_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def start_parse_resume_task(request):
    resume_id = request.data.get('resume_id')
    if resume_id:
        task = parse_resume_save_in_db_task.delay(resume_id)
        return Response({'task_id': task.id}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Resume ID is required'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def check_parse_resume_task_status(request, task_id):
    task_result = AsyncResult(task_id)
    return Response({'task_id': task_id, 'status': task_result.status}, status=status.HTTP_200_OK)
