from django.db import models
from django.contrib.auth.models import User


class ReferralCode(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='referral_code')
    code = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"ReferralCode({self.user.username}, {self.code})"


class Referral(models.Model):
    referred_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='referrals_made')
    referred_user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='referred_by')
    code_used = models.ForeignKey(ReferralCode, on_delete=models.CASCADE)

    def __str__(self):
        return f"Referral({self.referred_by.username} -> {self.referred_user.username})"
