from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
from django.shortcuts import render
from django.utils import timezone
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Resume, CoverLetter, OnboardingDetails
from .serializers import ResumeSerializer, CoverLetterSerializer
from rest_framework.decorators import api_view
from .aiparser import parse_resume_save_in_db_task
from celery.result import AsyncResult
from django.http import JsonResponse
from langchain_vectordb.utils import resume_query, resume_query2
import json
from django.shortcuts import get_object_or_404
from langchain_vectordb.utils import create_chat_model_for_resume, get_chat_model_from_resume


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

    # remove older resumes
    Resume.objects.filter(user=request.user).all().delete()

    resume = Resume(file=file)
    resume.filename = file_name
    resume.submitted_at = timezone.now()
    resume.user = request.user  # Assuming you have a user field and the user is logged in
    # ... set other fields as needed
    resume.save()

    # Serialize the resume after saving
    resume_serializer = ResumeSerializer(resume)
    return JsonResponse(resume_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def onboarding_details(request):
    if request.method == 'POST':
        user = request.user
        data = json.dumps(request.data)
        obd, created = OnboardingDetails.objects.get_or_create(user=user)
        obd.data = data
        obd.save()
        return JsonResponse({"message": "successful"}, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        user = request.user
        try:
            obd = OnboardingDetails.objects.get(user=user)
            return JsonResponse(json.loads(obd.data), status=status.HTTP_200_OK)
        except OnboardingDetails.DoesNotExist:
            return JsonResponse({"error": "Onboarding details not found."}, status=status.HTTP_200_OK)


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

        # coverletter remove
    CoverLetter.objects.filter(user=request.user).all().delete()

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
    # print(query)
    if not resume_id or not query:
        return Response({'error': 'Resume ID and query are required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        resume = Resume.objects.get(id=resume_id)
        response = resume_query(resume, query)
        return JsonResponse({"response": response}, status=status.HTTP_200_OK)
    except Resume.DoesNotExist:
        return Response({'error': 'Resume not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def resume_query_view2(request):
    print("resume 2 api started")

    # Extracting data from the request
    resume_id = request.data.get('resume_id')
    queries = request.data.get('queries')

    # Validating the presence of necessary data
    if not resume_id or not queries:
        return Response({'error': 'Resume ID and queries are required'},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        # Fetching the resume object
        resume = Resume.objects.get(id=resume_id)
        if not resume.chat_model:
            create_chat_model_for_resume(resume)
        chat_model = get_chat_model_from_resume(resume)

        responses = []
        error_response = None

        def handle_query(query):
            # Function to handle individual queries
            nonlocal error_response
            try:
                response, error = resume_query2(chat_model, query)
                if error:
                    error_response = error
                    raise Exception(error)
                return {'response': response, 'query': query}
            except Exception as e:
                return {'error': str(e), 'query': query}

        # Parallel processing of queries
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(
                handle_query, query): query for query in queries}
            for future in as_completed(futures):
                result = future.result()  # Apply timeout here if necessary
                if 'error' in result:
                    break
                responses.append(result)

        if error_response:
            print("hell yeah")
            print(error_response)
            if (error_response.status_code == 429):
                return error_response
            return JsonResponse({"responses": [], "error": "Timeout error"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            # return error_response
        return JsonResponse({"responses": responses}, status=status.HTTP_200_OK)

    except Resume.DoesNotExist:
        return Response({'error': 'Resume not found'},
                        status=status.HTTP_404_NOT_FOUND)
