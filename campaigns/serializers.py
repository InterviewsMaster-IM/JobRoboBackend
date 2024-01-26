from rest_framework import serializers
from .models import Campaign, ScrapedJob


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'


class ScrapedJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapedJob
        fields = '__all__'
