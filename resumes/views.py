from django.shortcuts import render
from django.utils import timezone
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Resume, CoverLetter
from .serializers import ResumeSerializer, CoverLetterSerializer
from rest_framework.decorators import api_view
from .aiparser import parse_resume_save_in_db_task
from celery.result import AsyncResult
from django.http import JsonResponse
from langchain_vectordb.utils import resume_query


@api_view(['POST'])
def resume_upload(request):
    # Validate the necessary fields
    file = request.data.get('file')
    if not file:
        return Response({'error': 'File is required'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the file is in the allowed format (pdf, docx, txt)
    file_name = file.name.lower()
    if not (file_name.endswith('.pdf') or file_name.endswith('.docx') or file_name.endswith('.txt')):
        return Response({'error': 'File must be a PDF, DOCX, or TXT format'}, status=status.HTTP_400_BAD_REQUEST)

    # Check for file size less than 5MB
    if file.size > 5 * 1024 * 1024:
        return Response({'error': 'File size must be less than 5MB'}, status=status.HTTP_400_BAD_REQUEST)

    resume = Resume(file=file)
    resume.filename = file_name
    resume.submitted_at = timezone.now()
    resume.user = request.user  # Assuming you have a user field and the user is logged in
    # ... set other fields as needed
    resume.save()

    # Serialize the resume after saving
    resume_serializer = ResumeSerializer(resume)
    return JsonResponse(resume_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def coverletter_upload(request):
    # Validate the necessary fields
    file = request.data.get('file')
    if not file:
        return Response({'error': 'File is required'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the file is in the allowed format (pdf, docx, txt)
    file_name = file.name.lower()
    if not (file_name.endswith('.pdf') or file_name.endswith('.docx') or file_name.endswith('.txt')):
        return Response({'error': 'File must be a PDF, DOCX, or TXT format'}, status=status.HTTP_400_BAD_REQUEST)

    # Check for file size less than 5MB
    if file.size > 5 * 1024 * 1024:
        return Response({'error': 'File size must be less than 5MB'}, status=status.HTTP_400_BAD_REQUEST)

    coverletter = CoverLetter(file=file)
    coverletter.filename = file_name
    coverletter.submitted_at = timezone.now()
    # Assuming you have a user field and the user is logged in
    coverletter.user = request.user
    # ... set other fields as needed
    coverletter.save()

    # Serialize the cover letter after saving
    coverletter_serializer = CoverLetterSerializer(coverletter)
    return JsonResponse(coverletter_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def delete_resume(request, resume_id):
    try:
        resume = Resume.objects.get(id=resume_id, user=request.user)
        resume.delete()
        return Response({'message': 'Resume deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Resume.DoesNotExist:
        return Response({'error': 'Resume not found or not owned by user'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_coverletter(request, coverletter_id):
    try:
        coverletter = CoverLetter.objects.get(
            id=coverletter_id, user=request.user)
        coverletter.delete()
        return Response({'message': 'Cover letter deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except CoverLetter.DoesNotExist:
        return Response({'error': 'Cover letter not found or not owned by user'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_uploads(request):
    try:
        resume = Resume.objects.filter(
            user=request.user).order_by('-created_time')[0]
        resume_data = ResumeSerializer(resume).data
    except IndexError:
        resume_data = None

    try:
        coverletter = CoverLetter.objects.filter(
            user=request.user).order_by('-created_time')[0]
        coverletter_data = CoverLetterSerializer(coverletter).data
    except IndexError:
        coverletter_data = None
    return Response({'resume': resume_data, 'coverletter': coverletter_data})


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


@api_view(['POST'])
def resume_query_view(request):
    resume_id = request.data.get('resume_id')
    query = request.data.get('query')
    if not resume_id or not query:
        return Response({'error': 'Resume ID and query are required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        resume = Resume.objects.get(id=resume_id)
        response = resume_query(resume, query)
        return JsonResponse({"response": response}, status=status.HTTP_200_OK)
    except Resume.DoesNotExist:
        return Response({'error': 'Resume not found'}, status=status.HTTP_404_NOT_FOUND)
