from django.contrib import admin
from .models import Skill, WorkExperience, Education, PersonalInfo

# Register your models here.
admin.site.register(Skill)
admin.site.register(WorkExperience)
admin.site.register(Education)
admin.site.register(PersonalInfo)
