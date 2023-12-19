from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
import urllib
import requests
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

def linkedin_login(request):
    params = {
        'response_type': 'code',
        'client_id': settings.LINKEDIN_CLIENT_ID,
        'redirect_uri': settings.LINKEDIN_REDIRECT_URI,
        'scope': settings.LINKEDIN_SCOPE
    }
    url = f'{settings.LINKEDIN_AUTHORIZATION_URL}?{urllib.parse.urlencode(params)}'
    return redirect(url)

def linkedin_callback(request):
    code = request.GET.get('code')
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.LINKEDIN_REDIRECT_URI,
        'client_id': settings.LINKEDIN_CLIENT_ID,
        'client_secret': settings.LINKEDIN_CLIENT_SECRET
    }
    response = requests.post(settings.LINKEDIN_ACCESS_TOKEN_URL, data=data)
    access_token = response.json().get('access_token')
    # fetch details
    data_response = requests.get(
        'https://api.linkedin.com/v2/userinfo',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    data = data_response.json()

    # Create user if user doesn't exist
    user,created = User.objects.get_or_create(username=data['sub'], defaults={
        'first_name':data.get('given_name'),
        'last_name':data.get('family_name')
    })

    refresh = RefreshToken.for_user(user)
    tokens = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
    # Redirect to frontend with tokens
    redirect_url = f"{settings.TOKEN_HANDLER_URL}?access={tokens['access']}&refresh={tokens['refresh']}"
    return redirect(redirect_url)

