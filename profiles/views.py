from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import OtherDetails
from .serializers import OtherDetailsSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_other_details(request):
    """
    Add other details for a user.
    """
    serializer = OtherDetailsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_other_details(request):
    """
    Retrieve other details for a user.
    """
    try:
        other_details = OtherDetails.objects.get(user=request.user)
        serializer = OtherDetailsSerializer(other_details)
        return Response(serializer.data)
    except OtherDetails.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
