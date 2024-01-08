from django.db.models import Sum
from rest_framework import generics, views, status
from rest_framework.response import Response
from .models import CreditPlan, UserCredits
from .serializers import CreditPlanSerializer, UserCreditsSerializer
from django.contrib.auth.models import User
from django.db.models import Case, When, Value, IntegerField


# Assuming you have the serializers defined for each model


class CreditPlanListView(generics.ListAPIView):
    queryset = CreditPlan.objects.filter(type='PAID').all()
    serializer_class = CreditPlanSerializer


class UserCreditsView(views.APIView):
    def get(self, request, *args, **kwargs):
        user_credits = UserCredits.objects.filter(user=request.user)
        total_credits = user_credits.aggregate(
            Sum('plan__credits'))['plan__credits__sum'] or 0
        credits_by_plan = user_credits.values('plan__name').annotate(
            total=Sum('plan__credits')).order_by('plan')
        # get currentplan
        uc = UserCredits.objects.filter(user=request.user).annotate(
            custom_order=Case(
                When(plan__type='PAID', then=Value(1)),
                When(plan__type='EARNED', then=Value(2)),
                When(plan__type='FREE', then=Value(3)),
                default=Value(4),
                output_field=IntegerField(),
            )).order_by('custom_order')
        currentplan = None
        if (uc.exists()):
            currentplan = CreditPlanSerializer(uc[0].plan).data

        data = {
            'total_credits': total_credits,
            'credits_by_plan': credits_by_plan,
            'current_plan': currentplan
        }

        return Response(data)


class CreditHistoryView(views.APIView):
    def get(self, request, *args, **kwargs):
        credit_history = UserCredits.objects.filter(user=request.user)
        serializer = UserCreditsSerializer(credit_history, many=True)
        return Response(serializer.data)
