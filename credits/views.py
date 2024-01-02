from rest_framework import generics, views, status
from rest_framework.response import Response
from .models import CreditPlan, UserCredits
from .serializers import CreditPlanSerializer, UserCreditsSerializer
from django.contrib.auth.models import User

# Assuming you have the serializers defined for each model


class CreditPlanListView(generics.ListAPIView):
    queryset = CreditPlan.objects.all()
    serializer_class = CreditPlanSerializer


class UserCreditsView(views.APIView):
    def get(self, request, *args, **kwargs):
        user_credits = UserCredits.objects.filter(user=request.user)
        total_credits = user_credits.aggregate(
            Sum('credits'))['credits__sum'] or 0
        credits_by_plan = user_credits.values('plan__name').annotate(
            total=Sum('credits')).order_by('plan')
        data = {
            'total_credits': total_credits,
            'credits_by_plan': credits_by_plan
        }
        return Response(data)


class CreditHistoryView(views.APIView):
    def get(self, request, *args, **kwargs):
        credit_history = UserCredits.objects.filter(user=request.user)
        serializer = UserCreditsSerializer(credit_history, many=True)
        return Response(serializer.data)
