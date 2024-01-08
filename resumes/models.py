from django.db import models
from django.conf import settings

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute

import os
import uuid
from django.utils.deconstruct import deconstructible


@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.sub_path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(uuid.uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.sub_path, filename)


path_and_rename_resume = PathAndRename("resumes")
path_and_rename_coverletter = PathAndRename("coverletters")
path_and_rename_chatmodel = PathAndRename("cht_mdl")


class Resume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    file = models.FileField(upload_to=path_and_rename_resume)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    chat_model = models.FileField(
        upload_to=path_and_rename_chatmodel, null=True)

    def __str__(self):
        return f"Resume {self.id} of user {self.user_id}"


class CoverLetter(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    file = models.FileField(upload_to=path_and_rename_coverletter)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    chat_model = models.FileField(
        upload_to=path_and_rename_chatmodel, null=True)

    def __str__(self):
        return f"Coverletter {self.id} of user {self.user_id}"
