from django.db import models
from django.conf import settings

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute

# Create your models here.


class Resume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    file = models.FileField(upload_to="resumes/")
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    #
    chat_model = models.FileField(upload_to="cht_mdl/", null=True)

    def __str__(self):
        return f"Resume {self.id} of user {self.user_id}"


class CoverLetter(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    file = models.FileField(upload_to="coverletters/")
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    #
    chat_model = models.FileField(upload_to="cht_mdl/", null=True)

    def __str__(self):
        return f"Coverletter {self.id} of user {self.user_id}"
