from django.db import models
import uuid
from django.conf import settings
from resumes.models import Resume
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Campaign(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    campaign_keyword = models.CharField(max_length=255, blank=True)
    campaign_type = models.CharField(max_length=255, blank=True)
    job_board = models.CharField(max_length=255, blank=True)
    jobs_applied = models.IntegerField(default=0, blank=True)
    country_selected = models.CharField(max_length=255, blank=True)
    job_type = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    resume = models.ForeignKey(Resume, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.campaign_keyword} - {self.job_board}"


class ScrapedJob(models.Model):
    campaign = models.ForeignKey(
        Campaign, related_name='scraped_jobs', on_delete=models.CASCADE, blank=True)
    job_source = models.CharField(max_length=255, blank=True)
    company_name = models.CharField(max_length=255, blank=True)
    posted_contact = models.CharField(max_length=255, blank=True)
    apply_type = models.CharField(max_length=255, blank=True)
    job_url = models.URLField(blank=True)
    job_location = models.CharField(max_length=255, blank=True)
    job_location_city = models.CharField(max_length=255, blank=True)
    job_location_state = models.CharField(max_length=255, blank=True)
    job_location_country = models.CharField(max_length=255, blank=True)
    job_location_zip = models.CharField(max_length=255, blank=True)
    job_title = models.CharField(max_length=255, blank=True)
    job_type = models.CharField(max_length=255, blank=True)
    work_type = models.CharField(max_length=255, blank=True)
    job_description = models.TextField(blank=True)
    is_visa_required = models.BooleanField(default=False, blank=True)
    date_posted = models.DateField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"{self.job_title} - {self.company_name}"

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            self.campaign.jobs_applied = ScrapedJob.objects.filter(
                campaign=self.campaign).count()
            self.campaign.save()


@receiver(post_delete, sender=ScrapedJob)
def update_jobs_applied_on_delete(sender, instance, **kwargs):
    campaign = instance.campaign
    campaign.jobs_applied = ScrapedJob.objects.filter(
        campaign=campaign).count()
    campaign.save()


# Connect the signal
post_delete.connect(update_jobs_applied_on_delete, sender=ScrapedJob)
