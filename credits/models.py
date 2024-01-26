from django.conf import settings
from django.db import models


class CreditPlan(models.Model):
    PLAN_TYPES = [
        ('PAID', 'Paid'),
        ('FREE', 'Free'),
        ('EARNED', 'Earned'),
    ]

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    credits = models.IntegerField()
    expiry_duration = models.DurationField()
    type = models.CharField(max_length=6, choices=PLAN_TYPES)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class UserCredits(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    plan = models.ForeignKey(CreditPlan, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.date.strftime('%Y-%m-%d %H:%M:%S')}"


class UserCreditUsage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    plan = models.ForeignKey(CreditPlan, on_delete=models.PROTECT, null=True)
    credits_used = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.date.strftime('%Y-%m-%d %H:%M:%S')}"
