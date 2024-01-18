from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def skill_list_create_view(request):
    if request.method == 'GET':
        skills = Skill.objects.filter(user=request.user)
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        data['user'] = request.user.pk
        serializer = SkillSerializer(data=data)
        if serializer.is_valid():
            # remove old skills
            Skill.objects.filter(user=request.user).all().delete()
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def skill_detail_view(request, pk):
    skill = get_object_or_404(Skill, pk=pk, user=request.user)
    if request.method == 'GET':
        serializer = SkillSerializer(skill)
        return Response(serializer.data)
    elif request.method == 'PUT':
        data = request.data
        data['user'] = request.user.pk
        serializer = SkillSerializer(skill, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# WorkExperience Views


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def work_experience_list_create_view(request):
    if request.method == 'GET':
        work_experiences = WorkExperience.objects.filter(user=request.user)
        serializer = WorkExperienceSerializer(work_experiences, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data.copy()  # Create a mutable copy of the request data
        # Set the user to the logged in user's id
        data['user'] = request.user.pk
        serializer = WorkExperienceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def work_experience_detail_view(request, pk):
    work_experience = get_object_or_404(
        WorkExperience, pk=pk, user=request.user)
    if request.method == 'GET':
        serializer = WorkExperienceSerializer(work_experience)
        return Response(serializer.data)
    elif request.method == 'PUT':
        data = request.data.copy()  # Create a mutable copy of the request data
        # Set the user to the logged in user's id
        data['user'] = request.user.pk
        serializer = WorkExperienceSerializer(work_experience, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        work_experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Education Views


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def education_list_create_view(request):
    if request.method == 'GET':
        educations = Education.objects.filter(user=request.user)
        serializer = EducationSerializer(educations, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data.copy()  # Create a mutable copy of the request data
        # Set the user to the logged in user's id
        data['user'] = request.user.pk
        serializer = EducationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def education_detail_view(request, pk):
    education = get_object_or_404(Education, pk=pk, user=request.user)
    if request.method == 'GET':
        serializer = EducationSerializer(education)
        return Response(serializer.data)
    elif request.method == 'PUT':
        data = request.data.copy()  # Create a mutable copy of the request data
        # Set the user to the logged in user's id
        data['user'] = request.user.pk
        serializer = EducationSerializer(education, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        education.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# PersonalInfo Views


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def personal_info_view(request):
    personal_info, created = PersonalInfo.objects.get_or_create(
        user=request.user)
    if request.method == 'GET':
        serializer = PersonalInfoSerializer(personal_info)
        return Response(serializer.data)
    elif request.method == 'PUT':
        data = request.data.copy()  # Create a mutable copy of the request data
        # Set the user to the logged in user's id
        data['user'] = request.user.pk
        serializer = PersonalInfoSerializer(personal_info, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
