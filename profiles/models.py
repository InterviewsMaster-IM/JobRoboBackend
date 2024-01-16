from django.db import models
from django.conf import settings
from django.utils import timezone


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


class Skill(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    skill = models.CharField(max_length=100)
    years_of_experience = models.DecimalField(max_digits=4, decimal_places=1)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.skill} ({self.years_of_experience} years)"


class WorkExperience(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    position_title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('temporary', 'Temporary'),
        ('volunteer', 'Volunteer'),
        ('other', 'Other'),
    ]
    employment_type = models.CharField(
        max_length=20, choices=EMPLOYMENT_TYPE_CHOICES)
    current_role = models.BooleanField()
    start_month_year = models.DateField()
    end_month_year = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.position_title} at {self.company_name}"


class Education(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    school = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    major_field_of_study = models.CharField(max_length=100)
    start_month_year = models.DateField()
    end_month_year = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.degree} in {self.major_field_of_study} from {self.school}"


class PersonalInfo(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=128, blank=True)
    last_name = models.CharField(max_length=128, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    country_code = models.CharField(max_length=3, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    dob = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"PersonalInfo({self.user.username})"
