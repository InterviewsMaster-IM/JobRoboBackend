from django.db import models
import secrets


class JobBoard(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class JobRobo(models.Model):
    JOB_TYPE_CHOICES = [
        ('onsite', 'Onsite'),
        ('hybrid', 'Hybrid'),
        ('remote', 'Remote'),
    ]
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    uid = models.CharField(max_length=6, unique=True, blank=True)
    job_title = models.CharField(max_length=255)
    job_types = models.ManyToManyField('JobType', related_name='job_robos')
    location = models.CharField(max_length=255)
    number_of_jobs_to_apply = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    job_board = models.ForeignKey(
        JobBoard, on_delete=models.CASCADE, related_name='job_robos')

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = secrets.token_urlsafe(6)[:6]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"JobRobo({self.user.username}, {self.created})"


class JobType(models.Model):
    name = models.CharField(null=True, max_length=32, unique=True)

    def __str__(self):
        return self.name
