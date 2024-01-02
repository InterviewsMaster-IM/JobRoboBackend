from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from .models import ReferralCode, Referral
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
def create_referral_code(request):
    user = request.user
    if hasattr(user, 'referral_code'):
        return JsonResponse({'error': 'Referral code already exists'}, status=status.HTTP_400_BAD_REQUEST)

    referral_code = ReferralCode.objects.create(
        user=user, code=User.objects.make_random_password())
    return JsonResponse({'referral_code': referral_code.code}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def validate_referral_code(request, code):
    try:
        referral_code = ReferralCode.objects.get(code=code)
    except ReferralCode.DoesNotExist:
        return JsonResponse({'error': 'Invalid referral code'}, status=status.HTTP_400_BAD_REQUEST)

    referred_user = request.user
    if Referral.objects.filter(referred_user=referred_user).exists():
        return JsonResponse({'error': 'User already referred'}, status=status.HTTP_400_BAD_REQUEST)

    Referral.objects.create(referred_by=referral_code.user,
                            referred_user=referred_user, code_used=referral_code)
    return JsonResponse({'message': 'Referral code accepted'}, status=status.HTTP_200_OK)
