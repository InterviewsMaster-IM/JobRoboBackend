# credits/serializers.py
from rest_framework import serializers
from .models import CreditPlan, UserCredits


class CreditPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditPlan
        fields = '__all__'


class UserCreditsSerializer(serializers.ModelSerializer):
    plan = CreditPlanSerializer(read_only=True)

    class Meta:
        model = UserCredits
        fields = '__all__'
