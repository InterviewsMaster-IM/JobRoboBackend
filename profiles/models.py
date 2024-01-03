from django.db import models
from django.conf import settings


class OtherDetails(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    RACE_CHOICES = [
        ('hispanic_latino', 'Hispanic or Latino'),
        ('americanIndian_alaskaNative', 'American Indian or Alaska Native'),
        ('asian', 'Asian'),
        ('black_africanAmerican', 'Black or African American'),
        ('hawaiian', 'Native Hawaiian or Other Pacific Islander'),
        ('two_or_more', 'Two or More Races'),
        ('white', 'White'),
        ('none', 'Prefer not to specify'),
    ]

    VETERAN_STATUS_CHOICES = [
        ('no', 'I am not a protected veteran'),
        ('yes', 'I identify as one or more of the classifications of protected veteran listed above'),
        ('none', 'Prefer not to specify'),
    ]

    DISABILITY_STATUS_CHOICES = [
        ('yes', 'Yes, I have a disability, or have had one in the past'),
        ('no', 'No, I do not have a disability and have not had one in the past'),
        ('none', 'Prefer not to answer'),
    ]

    WORK_PREFERENCE_CHOICES = [
        ('onsite', 'Onsite'),
        ('hybrid', 'Hybrid'),
        ('remote', 'Remote'),
    ]

    SALARY_CURRENCY_CHOICES = [
        ('usd', 'USD'),
        ('eur', 'EUR'),
        ('gbp', 'GBP'),
        ('inr', 'INR'),
        ('none', 'Prefer not to specify'),
    ]

    race = models.CharField(
        max_length=30, choices=RACE_CHOICES, default='none')
    veteran_status = models.CharField(
        max_length=10, choices=VETERAN_STATUS_CHOICES, default='none')
    disability_status = models.CharField(
        max_length=10, choices=DISABILITY_STATUS_CHOICES, default='none')
    notice_period = models.CharField(
        max_length=50, default='')
    desired_salary = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    desired_salary_currency = models.CharField(
        max_length=4, choices=SALARY_CURRENCY_CHOICES, default='none')
    work_authorization_status = models.BooleanField(default=True)
    visa_sponsorship_status = models.BooleanField(default=False)
    work_preference = models.CharField(
        max_length=10, choices=WORK_PREFERENCE_CHOICES, default='onsite')

    def __str__(self):
        return f"OtherDetails(race={self.race}, veteran_status={self.veteran_status}, disability_status={self.disability_status}, work_preference={self.work_preference}, notice_period={self.notice_period}, desired_salary={self.desired_salary}, desired_salary_currency={self.desired_salary_currency}, work_authorization_status={self.work_authorization_status}, visa_sponsorship_status={self.visa_sponsorship_status})"
