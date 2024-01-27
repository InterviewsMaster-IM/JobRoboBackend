from django.db.models import Case, When, Value, IntegerField
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Campaign, ScrapedJob
from resumes.models import Resume
import uuid
from django.shortcuts import get_object_or_404
from credits.models import CreditPlan, UserCredits, UserCreditUsage
from .serializers import *


@api_view(['GET'])
def get_user_campaigns(request):
    user = request.user
    if user.is_authenticated:
        campaigns = Campaign.objects.filter(user=user)
        serializer = CampaignSerializer(campaigns, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def get_campaign_jobs_applied(request, campaign_id):
    user = request.user
    if user.is_authenticated:
        campaign = get_object_or_404(Campaign, id=campaign_id, user=user)
        scraped_jobs = campaign.scraped_jobs.all()
        serializer = ScrapedJobSerializer(scraped_jobs, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def create_campaign(request):
    data = request.data
    try:
        # Convert resume_id from string to UUID
        resume_id = data.get('resumeId')
        resume = Resume.objects.get(id=resume_id)
        # Create a new Campaign instance
        campaign = Campaign(
            user=request.user,  # Assuming the user is authenticated
            campaign_keyword=data.get('campaignKeyword', ''),
            campaign_type=data.get('campaignType', ''),
            job_board=data.get('jobBoard', ''),
            jobs_applied=int(data.get('jobsApplied', 0)),
            country_selected=data.get('countrySelected', ''),
            job_type=data.get('jobType', ''),
            location=data.get('location', ''),
            resume=resume
        )
        # Save the new Campaign to the database
        campaign.save()

        # Prepare the response data
        response_data = {
            'id': campaign.id,
            'campaign_keyword': campaign.campaign_keyword,
            'campaign_type': campaign.campaign_type,
            'job_board': campaign.job_board,
            'jobs_applied': campaign.jobs_applied,
            'country_selected': campaign.country_selected,
            'job_type': campaign.job_type,
            'location': campaign.location,
            'resume_id': campaign.resume_id
        }

        # Return a success response
        return JsonResponse(response_data, status=status.HTTP_201_CREATED)

    except Exception as e:
        # Return an error response
        return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_campaign(request):
    data = request.data
    try:

        # update credits usage
        # get current plan
        uc = UserCredits.objects.filter(user=request.user).annotate(
            custom_order=Case(
                When(plan__type='PAID', then=Value(1)),
                When(plan__type='EARNED', then=Value(2)),
                When(plan__type='FREE', then=Value(3)),
                default=Value(4),
                output_field=IntegerField(),
            )).order_by('custom_order')
        # update usage of credits
        currentplan = None
        if (uc.exists()):
            currentplan = uc[0].plan
            ucu = UserCreditUsage(user=request.user, plan=currentplan,
                                  credits_used=len(data.get('scrapedJobs', [])))
            ucu.save()
        else:
            return JsonResponse({"error": "User doesn't have a valid plan"}, status=status.HTTP_200_OK)

        # Retrieve the campaign by ID
        campaign_id = data.get('campaignId')
        campaign = get_object_or_404(Campaign, id=campaign_id)

        # Update or create scraped jobs
        for job_data in data.get('scrapedJobs', []):
            ScrapedJob.objects.update_or_create(
                campaign=campaign,
                job_url=job_data.get('jobUrl'),
                defaults={
                    'job_source': job_data.get('jobSource', ''),
                    'company_name': job_data.get('companyName', ''),
                    'posted_contact': job_data.get('postedContact', ''),
                    'apply_type': job_data.get('applyType', ''),
                    'job_location': job_data.get('jobLocation', ''),
                    'job_location_city': job_data.get('jobLocationCity', ''),
                    'job_location_state': job_data.get('jobLocationState', ''),
                    'job_location_country': job_data.get('jobLocationCountry', ''),
                    'job_location_zip': job_data.get('jobLocationZip', ''),
                    'job_title': job_data.get('jobTitle', ''),
                    'job_type': job_data.get('jobType', ''),
                    'work_type': job_data.get('workType', ''),
                    'job_description': job_data.get('jobDescription', ''),
                    'is_visa_required': job_data.get('isVisaRequired', False),
                    # Assuming datePosted is in the correct format
                    'date_posted': job_data.get('datePosted')
                }
            )

        # Update the jobs_applied field
        # campaign.jobs_applied += data.get('jobsApplied', campaign.jobs_applied)
        campaign.save()

        # Return a success response
        return JsonResponse({'message': 'Campaign updated successfully'}, status=status.HTTP_200_OK)

    except Exception as e:
        # Return an error response
        return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
