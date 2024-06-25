from django.shortcuts import get_object_or_404
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import JobRobo, JobBoard, JobType
from .serializers import JobRoboSerializer, JobBoardSerializer, JobTypeSerializer


class JobRoboListCreateView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        jobrobos = JobRobo.objects.filter(user=request.user)
        serializer = JobRoboSerializer(jobrobos, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        job_board_name = request.data.get('job_board')
        job_board = JobBoard.objects.get(name=job_board_name)
        job_type_names = request.data.get('job_types', [])
        job_types = [JobType.objects.get(name=job_type_name)
                     for job_type_name in job_type_names]

        # Create a new JobRobo instance directly without using JobRoboSerializer
        job_robo_instance = JobRobo.objects.create(
            user=request.user,
            job_title=request.data.get('job_title'),
            location=request.data.get('location'),
            number_of_jobs_to_apply=request.data.get(
                'number_of_jobs_to_apply'),
            job_board=job_board
        )
        # Assign job_types instances
        job_robo_instance.job_types.set(job_types)
        # Save the instance with the new assignments
        job_robo_instance.save()

        # Manually construct the response data since we're not using JobRoboSerializer
        response_data = {
            'id': job_robo_instance.id,
            'user': request.user.id,  # Assuming the user wants the user ID in the response
            'uid': job_robo_instance.uid,
            'job_title': job_robo_instance.job_title,
            'location': job_robo_instance.location,
            'number_of_jobs_to_apply': job_robo_instance.number_of_jobs_to_apply,
            'job_board': job_robo_instance.job_board.id,
            'job_types': [job_type.id for job_type in job_types]
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class JobBoardListView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        jobboards = JobBoard.objects.all()
        serializer = JobBoardSerializer(jobboards, many=True)
        return Response(serializer.data)


class JobTypeListView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        jobtypes = JobType.objects.all()
        serializer = JobTypeSerializer(jobtypes, many=True)
        return Response(serializer.data)
